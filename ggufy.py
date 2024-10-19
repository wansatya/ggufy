#!/usr/bin/env python3

import argparse
import requests
import os
import sys
import json
import hashlib
from llama_cpp import Llama
from tqdm import tqdm

CONFIG_DIR = os.path.expanduser("~/.config/ggufy")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
CACHE_DIR = os.path.expanduser("~/.cache/ggufy")

def save_token(token):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump({"token": token}, f)
    print("Token saved successfully.")

def load_token():
    try:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
        return config.get("token")
    except FileNotFoundError:
        return None

def get_headers(token):
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}

def parse_model_path(model_path):
    parts = model_path.split(':')
    repo_path = parts[0]
    file_name = parts[1] if len(parts) > 1 else 'latest'
    
    repo_parts = repo_path.split('/')
    if len(repo_parts) < 3 or repo_parts[0] != 'hf.co':
        raise ValueError(f"Invalid repository path: {repo_path}. Expected format: hf.co/username/repo")
    
    username = repo_parts[1]
    repo = '/'.join(repo_parts[2:])
    return username, repo, file_name

def find_latest_gguf(username, repo, token):
    print(f"Searching for GGUF files in {username}/{repo}...")
    api_url = f"https://huggingface.co/api/models/{username}/{repo}"
    response = requests.get(api_url, headers=get_headers(token))
    response.raise_for_status()
    files = response.json().get("siblings", [])
    gguf_files = [file["rfilename"] for file in files if file["rfilename"].endswith(".gguf")]
    
    if not gguf_files:
        raise ValueError(f"No GGUF file found in {username}/{repo}")
    
    latest_file = max(gguf_files)
    print(f"Latest GGUF file found: {latest_file}")
    return latest_file

def get_cached_model_path(username, repo, gguf_file):
    # Create a unique filename based on the model path
    model_id = hashlib.md5(f"{username}/{repo}/{gguf_file}".encode()).hexdigest()
    return os.path.join(CACHE_DIR, f"ggufy-{model_id}.gguf")

def download_model(model_path, token):
    username, repo, file_name = parse_model_path(model_path)
    
    if file_name == 'latest':
        gguf_file = find_latest_gguf(username, repo, token)
    else:
        gguf_file = file_name
    
    cached_path = get_cached_model_path(username, repo, gguf_file)
    
    if os.path.exists(cached_path):
        print(f"Using cached model: {cached_path}")
        return cached_path, gguf_file
    
    model_url = f"https://huggingface.co/{username}/{repo}/resolve/main/{gguf_file}"
    
    print(f"Downloading model: {gguf_file}")
    response = requests.get(model_url, stream=True, headers=get_headers(token))
    if response.status_code == 404:
        raise ValueError(f"GGUF file '{gguf_file}' not found in {username}/{repo}")
    response.raise_for_status()
    
    total_size = int(response.headers.get('content-length', 0))
    
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(cached_path, 'wb') as file:
        progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)
        for chunk in response.iter_content(chunk_size=8192):
            size = file.write(chunk)
            progress_bar.update(size)
        progress_bar.close()
    
    print(f"Model downloaded and cached: {cached_path}")
    return cached_path, gguf_file

def run_gguf_model(model_path, context, max_tokens, token):
    try:
        print("Initializing GGUFY Runner...")
        model_file, gguf_file = download_model(model_path, token)
        print(f"Model file: {model_file}")
        
        print("Loading model into memory...")
        llm = Llama(model_path=model_file, n_ctx=context)
        print("Model loaded successfully.")
        
        while True:
            prompt = input("Enter your prompt (or 'quit' to exit): ").strip()
            if prompt.lower() == 'quit':
                break
            
            print(f"Generating text with prompt: '{prompt}'")
            output = llm(prompt, max_tokens=max_tokens)
            
            print("\nGenerated text:")
            print(output['choices'][0]['text'])
            print("\n" + "-"*50 + "\n")
    
    except Exception as e:
        print(f"An error occurred: {e}")

def login():
    token = input("Enter your Hugging Face API token: ").strip()
    save_token(token)

def main():
    parser = argparse.ArgumentParser(description="Run GGUF models from Hugging Face Hub")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Login command
    login_parser = subparsers.add_parser("login", help="Save Hugging Face API token")

    # Run command
    run_parser = subparsers.add_parser("run", help="Run a GGUF model")
    run_parser.add_argument("model_path", help="Model path in the format hf.co/username/repo or hf.co/username/repo:latest or hf.co/username/repo:specific_file.gguf")
    run_parser.add_argument("-c", "--context", type=int, default=4096, help="Context size for the model")
    run_parser.add_argument("-t", "--max-tokens", type=int, default=200, help="Maximum number of tokens to generate")

    args = parser.parse_args()

    if args.command == "login":
        login()
    elif args.command == "run":
        token = load_token()
        if not token:
            print("No API token found. Please run 'ggufy login' first.")
            sys.exit(1)
        try:
            run_gguf_model(args.model_path, args.context, args.max_tokens, token)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()