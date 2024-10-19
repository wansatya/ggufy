#!/bin/bash

set -e

# Configuration
INSTALL_DIR="$HOME/.ggufy"
VENV_NAME="$INSTALL_DIR/venv"
SCRIPT_NAME="ggufy.py"
SCRIPT_URL="https://raw.githubusercontent.com/wansatya/ggufy/main/ggufy.py"
RUNNER_NAME="ggufy"

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3 and try again."
    exit 1
fi

# Create installation directory
mkdir -p "$INSTALL_DIR"

# Create virtual environment
python3 -m venv "$VENV_NAME"

# Activate virtual environment
source "$VENV_NAME/bin/activate"

# Install required packages
pip install --upgrade pip
pip install llama-cpp-python requests tqdm

# Download the Python script
curl -o "$INSTALL_DIR/$SCRIPT_NAME" "$SCRIPT_URL"
chmod +x "$INSTALL_DIR/$SCRIPT_NAME"

# Create runner script
cat > "$INSTALL_DIR/$RUNNER_NAME" << EOL
#!/bin/bash
source "$VENV_NAME/bin/activate"
python3 "$INSTALL_DIR/$SCRIPT_NAME" "\$@"
deactivate
EOL

chmod +x "$INSTALL_DIR/$RUNNER_NAME"

# Add to PATH
SHELL_RC="$HOME/.bashrc"
if [[ "$SHELL" == *"zsh"* ]]; then
    SHELL_RC="$HOME/.zshrc"
fi

echo "export PATH=\$PATH:$INSTALL_DIR" >> "$SHELL_RC"

echo "Installation complete. Please restart your terminal or run 'source $SHELL_RC' to use ggufy command."
echo "------------------------------------"
echo "Start using ggufy: 'ggufy login' "
echo "You can now run 'ggufy run hf.co/username/repository [options]' from anywhere."