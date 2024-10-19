# GGUFY - GGUF Models Runner

GGUFY is a tool that allows you to download and run GGUF (GPT-Generated Unified Format) models from the Hugging Face Hub using the llama-cpp-python library.

## Prerequisites

- Bash shell (Linux or macOS terminal, or Git Bash for Windows)
- Python 3.7 or later
- curl (for downloading the script)

## Setup

1. Download and run the setup script:
   ```
   curl -sSL https://raw.githubusercontent.com/wansatya/ggufy/main/setup.sh | bash
   ```

2. Restart your terminal or run:
   ```
   source ~/.bashrc  # or ~/.zshrc if you're using Zsh
   ```

The setup script will automatically download the latest release of GGUFY.

## Usage

After setup, you can run GGUFY from anywhere using:

```
ggufy run <model_path> [options]
```

### Required Arguments

- `run`: The command to execute
- `<model_path>`: Model path on Hugging Face Hub. Can be in one of these formats:
  - `hf.co/username/repo` (will use the latest GGUF file)
  - `hf.co/username/repo:latest` (explicitly use the latest GGUF file)
  - `hf.co/username/repo:specific_file.gguf` (use a specific GGUF file)

### Optional Arguments

- `-c`, `--context`: Context size for the model (default: 4096)
- `-t`, `--max-tokens`: Maximum number of tokens to generate (default: 200)
- `-p`, `--prompt`: Prompt for text generation (default: "Explain quantum computing")

### Examples

Using the latest GGUF file with short-form arguments:
```bash
ggufy run hf.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF -c 4096 -t 200 -p "Explain quantum computing"
```

Using a specific GGUF file with long-form arguments:
```bash
ggufy run hf.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF:mistral-7b-instruct-v0.1.Q4_K_M.gguf --context 4096 --max-tokens 200 --prompt "Explain quantum computing"
```

Using a repository with a hyphenated name:
```bash
ggufy run hf.co/meta-llama/Llama-2-7b-chat-hf -c 4096 -t 200 -p "Explain quantum computing"
```

### Help

To see all available options and their descriptions, run:

```bash
ggufy run --help
```

## Updating GGUFY

To update GGUFY to the latest version, simply run the setup script again:

```bash
curl -sSL https://raw.githubusercontent.com/yourusername/ggufy/main/setup.sh | bash
```

## How it works

1. The setup script installs the latest release of GGUFY in a dedicated directory with its own virtual environment.
2. When running a model:
   - If no specific file is provided, the script finds the latest GGUF file from the specified Hugging Face repository.
   - The model is downloaded and saved to a temporary file.
   - The model is loaded using the llama-cpp-python library.
   - Text is generated based on the provided prompt and parameters.
   - After execution, the temporary model file is automatically deleted.

## Troubleshooting

1. If `ggufy` command is not found, make sure you've restarted your terminal or sourced your shell configuration file after running the setup script.

2. For any issues, try running the setup script again. It will reinstall the latest version of GGUFY and its dependencies.

3. Make sure you have an active internet connection for downloading models and updates.

4. If you encounter any Python-related errors, ensure you're using Python 3.7 or later.

5. If no GGUF file is found in the specified repository, or if the specified file doesn't exist, the script will raise an error.

6. If you're having trouble with arguments, make sure you're using the correct format: `-c` for context, `-t` for max tokens, and `-p` for prompt.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License

Copyright (c) 2024 WanSatya Campus.

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