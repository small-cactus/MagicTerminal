#!/bin/bash

# Total number of tasks to perform
TOTAL_TASKS=5 # Homebrew, Git, Python 3.11, Python dependencies, API key and command setup
COMPLETED_TASKS=0

# Function to update progress and clear the screen
update_progress() {
    clear
    COMPLETED_ACTION=$1
    ((COMPLETED_TASKS++))
    PERCENTAGE=$((COMPLETED_TASKS * 100 / TOTAL_TASKS))
    echo "$COMPLETED_ACTION completed. Progress: $PERCENTAGE%. Continuing in 1 second..."
    sleep 1
    clear
}

# Function to install a Homebrew package if it's not already installed
install_if_not_present() {
    PACKAGE=$1
    if ! command -v $PACKAGE &> /dev/null
    then
        echo "Installing $PACKAGE..."
        brew install $PACKAGE
        update_progress "Installation of $PACKAGE"
    else
        echo "$PACKAGE is already installed."
        update_progress "$PACKAGE verification"
    fi
}

# Clear the screen initially
clear

# Check if Homebrew is installed
echo "Checking Homebrew installation..."
if ! command -v brew &> /dev/null
then
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    update_progress "Homebrew installation"
else
    echo "Homebrew is already installed."
    update_progress "Homebrew verification"
fi

# Install Git and Python 3.11
install_if_not_present git
install_if_not_present python@3.11

# Change directory to the script's directory
cd "$(dirname "$0")" || exit

# Install Python dependencies
echo "Installing Python dependencies..."
pip install openai # Add other necessary dependencies here
update_progress "Python dependencies installation"

# Ask for OpenAI API key
while true; do
    echo "Please enter your OpenAI API key (it should start with 'sk-'):"
    read -r api_key
    if [[ $api_key == sk-* ]]; then
        echo "api_key=\"$api_key\"" > apikey.py
        update_progress "API key setup"
        break
    else
        echo "The key you entered does not seem like an OpenAI API key. Please try again."
    fi
done

# Ask for preferred command name
echo "Choose your preferred command name (default: 'magic'). Type 'magic', 'miles' or your custom command:"
read -r command_name
command_name=${command_name:-magic}

# Append the chosen command function to .zshrc
FUNCTION_NAME=$command_name
FUNCTION_SCRIPT=$(cat <<EOF
$FUNCTION_NAME() {
    # Run the Python script with the provided arguments
    python3 $(pwd)/MagicTerminal.py "\$@"

    # Define the paths for the command and output files
    command_file='$(pwd)/command_to_run.txt'
    output_file='$(pwd)/command_output.txt'

    # Check if the command file exists and execute the command
    if [[ -f "\$command_file" ]]; then
        command_to_run=\$(cat "\$command_file")
        eval "\$command_to_run" &> "\$output_file"
        rm "\$command_file"
    fi
}
EOF
)

if ! grep -q "miles()" ~/.zshrc && ! grep -q "magic()" ~/.zshrc; then
    echo "$FUNCTION_SCRIPT" >> ~/.zshrc
    update_progress "Command function configuration"
else
    echo "Command function already present in .zshrc."
    update_progress "Command function verification"
fi

# Source the .zshrc file to apply changes
source ~/.zshrc

echo "Setup completed. You can now use '$FUNCTION_NAME' command in your terminal."
