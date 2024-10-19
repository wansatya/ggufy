#!/usr/bin/env python3

import argparse
import requests
import os
import sys
import json
import hashlib
import shutil
import time
import threading
from llama_cpp import Llama
from tqdm import tqdm

CONFIG_DIR = os.path.expanduser("~/.config/ggufy")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
CACHE_DIR = os.path.expanduser("~/.cache/ggufy")

def save_token(token):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump({"token": token}, f)
    print("Token saved successfully.\n")

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
    print(f"Searching for GGUF files in {username}/{repo}...\n")
    api_url = f"https://huggingface.co/api/models/{username}/{repo}"
    response = requests.get(api_url, headers=get_headers(token))
    response.raise_for_status()
    files = response.json().get("siblings", [])
    gguf_files = [file["rfilename"] for file in files if file["rfilename"].endswith(".gguf")]
    
    if not gguf_files:
        raise ValueError(f"No GGUF file found in {username}/{repo}")
    
    latest_file = max(gguf_files)
    print(f"Latest GGUF file found: {latest_file}\n")
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
        print(f"Using cached model: {cached_path}\n")
        return cached_path, gguf_file
    
    model_url = f"https://huggingface.co/{username}/{repo}/resolve/main/{gguf_file}"
    
    print(f"Downloading model: {gguf_file}\n")
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
    
    print(f"Model downloaded and cached: {cached_path}\n")
    return cached_path, gguf_file

def animated_loading():
    chars = ['    ', '.   ', '..  ', '... ']
    while getattr(threading.current_thread(), "do_run", True):
        for char in chars:
            sys.stdout.write('\r' + f"Generating {char}")
            sys.stdout.flush()
            time.sleep(0.8)
    sys.stdout.write('\r' + ' ' * 20 + '\r')
    sys.stdout.flush()

def run_gguf_model(model_path, context, max_tokens, token, force_cpu=False, stream=False):
    try:
        print("\nInitializing GGUFy...\n")
        model_file, gguf_file = download_model(model_path, token)
        print(f"Model file: {model_file}\n")
        
        print("Loading model into memory...\n")

        # Check for GPU availability
        gpu_layers = 0
        if not force_cpu:
            try:
                from llama_cpp import llama_cpp
                gpu_layers = llama_cpp.llama_n_gpu_layers
                print(f"GPU acceleration is available. Using {gpu_layers} GPU layers.\n")
            except AttributeError:
                print("GPU acceleration is not available. Using CPU.\n")
        else:
            print("Forced CPU usage. GPU will not be used even if available.\n")

        llm = Llama(model_path=model_file, n_ctx=context, n_gpu_layers=gpu_layers)
        print("\nModel loaded successfully.\n")
        
        while True:
            prompt = input("Any questions? (or 'quit' to exit): ").strip()
            if prompt.lower() == 'quit':
                break
            
            if stream:
                for chunk in llm(prompt, max_tokens=max_tokens, stream=True):
                    print(chunk['choices'][0]['text'], end='', flush=True)
                print("\n")
            else:
                # Start the loading animation
                loading_thread = threading.Thread(target=animated_loading)
                loading_thread.daemon = True
                loading_thread.start()
                
                # Generate text
                output = llm(prompt, max_tokens=max_tokens)
                
                # Stop the loading animation
                loading_thread.do_run = False
                loading_thread.join()
                
                print("\n")
                print(output['choices'][0]['text'])

            print("\n" + "-"*50 + "\n")
    
    except Exception as e:
        print(f"An error occurred: {e}")

def remove_ggufy():
    print("Removing GGUFy and all related files...\n")
    
    # Remove configuration directory
    if os.path.exists(CONFIG_DIR):
        shutil.rmtree(CONFIG_DIR)
        print(f"Removed configuration directory: {CONFIG_DIR}")
    
    # Remove cache directory
    if os.path.exists(CACHE_DIR):
        shutil.rmtree(CACHE_DIR)
        print(f"Removed cache directory: {CACHE_DIR}\n")
    
    # Remove the script itself
    script_path = os.path.abspath(__file__)
    os.remove(script_path)
    print(f"Removed GGUFy script: {script_path}\n")
    
    print("GGUFy has been successfully uninstalled.")
    print("Note: You may need to manually remove the 'ggufy' command from your PATH.\n")

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
    run_parser.add_argument("--cpu", action="store_true", help="Force CPU usage even if GPU is available")
    run_parser.add_argument("--stream", action="store_true", help="Enable streaming output")

    # Remove command
    remove_parser = subparsers.add_parser("remove", help="Uninstall GGUFy and remove all related files")

    args = parser.parse_args()

    if args.command == "login":
        login()
    elif args.command == "run":
        token = load_token()
        if not token:
            print("No API token found. Please run 'ggufy login' first.\n")
            sys.exit(1)
        try:
            run_gguf_model(args.model_path, args.context, args.max_tokens, token, force_cpu=args.cpu, stream=args.stream)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    elif args.command == "remove":
        confirm = input("Are you sure you want to uninstall GGUFy and remove all related files? (y/N): ").lower()
        if confirm == 'y':
            remove_ggufy()
        else:
            print("Uninstall cancelled.\n")
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()