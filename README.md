# **GGUFy** - GGUF Models Runner

**GGUFy** is a tool that allows you to download and run GGUF (GPT-Generated Unified Format) models from the Hugging Face Hub using the **llama-cpp-python** library.

## How it works

1. The setup script installs the latest release of **GGUFy** in a dedicated directory with its own virtual environment.

2. When running a model:

   - The script checks if the requested model is already cached in the `~/.cache/ggufy` directory.
   - If the model is cached, it uses the existing file.
   - If not, it downloads the model from the Hugging Face Hub and saves it to the cache directory.
   - The model is loaded into memory using the llama-cpp-python library.
   - You can input multiple prompts interactively, and the script will generate text based on each prompt.
   - Cached models are kept for future use, reducing download times for subsequent runs.


## Cache Management

**GGUFy** caches downloaded models in the `~/.cache/ggufy` directory. This helps to avoid re-downloading models you've used before. 

To manage the cache:

1. To clear the cache and free up space, you can manually delete the files in the `~/.cache/ggufy` directory.
2. If you want to force a re-download of a model, delete its corresponding file from the cache directory.


## Prerequisites

- Bash shell (Linux or macOS terminal, or Git Bash for Windows)
- Python 3.7 or later
- curl (for downloading the script)
- Hugging Face account and API token

## Setup

1. Create a Hugging Face account if you don't have one: [Hugging Face](https://huggingface.co/join)

2. Generate an API token:
   - Go to your [Hugging Face account settings](https://huggingface.co/settings/tokens)
   - Click on "New token"
   - Give it a name (e.g., "**GGUFy** Runner")
   - Select the appropriate permissions (read access is sufficient)
   - Copy the generated token

3. Download and run the setup script:
   ```
   curl -sSL https://raw.githubusercontent.com/wansatya/ggufy/main/setup.sh | bash
   ```

4. Restart your terminal or run:
   ```
   source ~/.bashrc  # or ~/.zshrc if you're using Zsh
   ```

5. Log in with your Hugging Face API token:
   ```
   ggufy login
   ```
   You will be prompted to enter your API token. This token will be saved for future use.

The setup script will automatically download the latest release of **GGUFy**.

## Usage

After setup and login, you can run **GGUFy** from anywhere using:

```bash
ggufy run <model_path> [options]
```

To see the help information, simply run:

```bash
ggufy run -h
```

### Commands

- `login`: Save your Hugging Face API token
- `run`: Run a GGUF model
- `remove`: Uninstall **GGUFy** and remove all related files

### Required Arguments for 'run' command

- `<model_path>`: Model path on Hugging Face Hub. Can be in one of these formats:
  - `hf.co/username/repo` (will use the latest GGUF file)
  - `hf.co/username/repo:latest` (explicitly use the latest GGUF file)
  - `hf.co/username/repo:specific_file.gguf` (use a specific GGUF file)

Note: The repository name can include hyphens or other special characters.

### Optional Arguments for 'run' command

- `-c`, `--context`: Context size for the model (default: 4096)
- `-t`, `--max-tokens`: Maximum number of tokens to generate (default: 200)

### Examples

Login:
```bash
ggufy login
```

Run the latest GGUF file with short-form arguments (GPU is available):

```bash
ggufy run hf.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF -c 4096 -t 200
```

Run a specific GGUF file with long-form arguments (CPU only):
```bash
ggufy run hf.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF:mistral-7b-instruct-v0.1.Q4_K_M.gguf --context 4096 --max-tokens 200 --cpu
```
After running one of these commands, you'll be prompted to enter your text prompts interactively.

## Uninstalling **GGUFy**

To uninstall **GGUFy** and remove all related files, run:
```bash
ggufy remove
```

This command will:

- Remove the configuration directory (`~/.config/ggufy`)
- Remove the cache directory (`~/.cache/ggufy`)
- Delete the **GGUFy** script itself

After running this command, you may need to manually remove the `ggufy` command from your PATH if you added it during installation.

## GPU Support

**GGUFy** automatically detects if GPU acceleration is available and uses it by default. If you want to force CPU usage, you can use the `--cpu` flag when running a model.

Note: GPU support requires a CUDA-compatible GPU and the appropriate CUDA libraries installed on your system.

## Troubleshooting

1. If `ggufy` command is not found, make sure you've restarted your terminal or sourced your shell configuration file after running the setup script.

2. For any issues, try running the setup script again. It will reinstall the latest version of **GGUFy** and its dependencies.

3. Make sure you have an active internet connection for downloading models and updates.

4. If you encounter any Python-related errors, ensure you're using Python 3.7 or later.

5. If no GGUF file is found in the specified repository, or if the specified file doesn't exist, the script will raise an error.

6. If you're having trouble with arguments, make sure you're using the correct format: `-c` for context and `-t` for max tokens.

7. If you're using a repository with a hyphenated name or other special characters, make sure to include the full repository name as it appears on Hugging Face.

8. If you encounter authentication issues, make sure you've run `ggufy login` and entered a valid Hugging Face API token. You can generate a new token in your Hugging Face account settings and run `ggufy login` again to update it.

9. If you're having issues with a cached model, try deleting the corresponding file from the `~/.cache/ggufy` directory to force a re-download.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License

Copyright (c) 2024 **GGUFy**.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.