#!/usr/bin/env python3

import argparse
import requests
import tempfile
import os
import sys
import json
from llama_cpp import Llama

CONFIG_DIR = os.path.expanduser("~/.config/ggufy")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

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
    
    username = repo_parts[2]
    repo = '/'.join(repo_parts[3:])
    return username, repo, file_name

def find_latest_gguf(username, repo, token):
    api_url = f"https://huggingface.co/api/models/{username}/{repo}"
    response = requests.get(api_url, headers=get_headers(token))
    response.raise_for_status()
    files = response.json().get("siblings", [])
    gguf_files = [file["rfilename"] for file in files if file["rfilename"].endswith(".gguf")]
    
    if not gguf_files:
        raise ValueError(f"No GGUF file found in {username}/{repo}")
    
    return max(gguf_files)  # Assuming the latest version has the highest lexicographic order

def download_model(model_path, token):
    username, repo, file_name = parse_model_path(model_path)
    
    if file_name == 'latest':
        gguf_file = find_latest_gguf(username, repo, token)
    else:
        gguf_file = file_name
    
    model_url = f"https://huggingface.co/{username}/{repo}/resolve/main/{gguf_file}"
    
    response = requests.get(model_url, stream=True, headers=get_headers(token))
    if response.status_code == 404:
        raise ValueError(f"GGUF file '{gguf_file}' not found in {username}/{repo}")
    response.raise_for_status()
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.gguf') as temp_file:
        for chunk in response.iter_content(chunk_size=8192):
            temp_file.write(chunk)
    
    return temp_file.name, gguf_file

def run_gguf_model(model_path, context, max_tokens, prompt, token):
    try:
        model_file, gguf_file = download_model(model_path, token)
        print(f"Model {gguf_file} downloaded and saved to: {model_file}")
        
        llm = Llama(model_path=model_file, n_ctx=context)
        
        output = llm(prompt, max_tokens=max_tokens)
        
        print("Generated text:")
        print(output['choices'][0]['text'])
    
    finally:
        if 'model_file' in locals():
            os.remove(model_file)

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
    run_parser.add_argument("-p", "--prompt", default="Explain quantum computing", help="Prompt for text generation")

    args = parser.parse_args()

    if args.command == "login":
        login()
    elif args.command == "run":
        token = load_token()
        if not token:
            print("No API token found. Please run 'ggufy login' first.")
            sys.exit(1)
        try:
            run_gguf_model(args.model_path, args.context, args.max_tokens, args.prompt, token)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()