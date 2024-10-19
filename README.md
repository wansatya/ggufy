# GGUFY - GGUF Models Runner

GGUFY is a tool that allows you to download and run GGUF (GPT-Generated Unified Format) models from the Hugging Face Hub using the llama-cpp-python library.

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
   - Give it a name (e.g., "GGUFY Runner")
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

The setup script will automatically download the latest release of GGUFY.

## Usage

After setup and login, you can run GGUFY from anywhere using:

```
ggufy run <model_path> [options]
```

To see the help information, simply run:

```
ggufy
```

### Commands

- `login`: Save your Hugging Face API token
- `run`: Run a GGUF model

### Required Arguments for 'run' command

- `<model_path>`: Model path on Hugging Face Hub. Can be in one of these formats:
  - `hf.co/username/repo` (will use the latest GGUF file)
  - `hf.co/username/repo:latest` (explicitly use the latest GGUF file)
  - `hf.co/username/repo:specific_file.gguf` (use a specific GGUF file)

Note: The repository name can include hyphens or other special characters.

### Optional Arguments for 'run' command

- `-c`, `--context`: Context size for the model (default: 4096)
- `-t`, `--max-tokens`: Maximum number of tokens to generate (default: 200)
- `-p`, `--prompt`: Prompt for text generation (default: "Explain quantum computing")

### Examples

Login:
```
ggufy login
```

Run the latest GGUF file with short-form arguments:
```
ggufy run hf.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF -c 4096 -t 200 -p "Explain quantum computing"
```

Run a specific GGUF file with long-form arguments:
```
ggufy run hf.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF:mistral-7b-instruct-v0.1.Q4_K_M.gguf --context 4096 --max-tokens 200 --prompt "Explain quantum computing"
```

[Rest of the README remains the same]

## Troubleshooting

[Add this to the existing Troubleshooting section]

8. If you encounter authentication issues, make sure you've run `ggufy login` and entered a valid Hugging Face API token. You can generate a new token in your Hugging Face account settings and run `ggufy login` again to update it.

[Rest of the README remains the same]

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