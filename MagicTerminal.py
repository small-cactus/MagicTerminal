#!/usr/bin/env python3
import openai
import json
import os
import subprocess
import threading
from apikey import api_key
import sys
import time
import datetime

# Set OpenAI API key
from openai import OpenAI
openai.api_key = api_key
client = OpenAI(api_key=api_key)

# Global variables
current_model = "gpt-4-0125-preview"  # Default model
system_prompt = """You are Miles, an AI terminal assistant operating in the user's MacOS terminal as part of MagicTerminal. Please follow these detailed guidelines:

1. COMMAND EXECUTION PROCEDURE:
   - Execute terminal commands using the 'RUN COMMAND' tool.
   - You have most admin privileges on the Users MacBook Pro.
   - Remember, commands are executed using the 'eval' method, which means they won't show up in the user's terminal interface.
   - IMPORTANT: Commands are only executed AFTER you run AND respond, which means you won't see the output until the user prompts you AGAIN to give the output.

2. OPTIMIZING COMMAND INPUT:
   - When possible, combine steps into multi-structured commands to minimize the need for user input.
   - Always try to find the necessary information yourself first. Only ask the user if it's essential or the task is too complex to automate.

3. CLARITY IN RESPONSES:
   - Aim to keep your responses concise, ideally one small sentence, this means RESPOND AS CONCISE AS POSSILBE.
   - If the situation requires a more detailed explanation, feel free to use longer responses for clarity.

4. USING PYTHON SCRIPTS:
   - For complex tasks, write and run Python scripts.
   - After completing the task, delete these scripts to keep the user's system clean and organized.

5. BROAD TERMINAL FUNCTIONS:
   - You can use the terminal for a wide array of tasks including searching for files, managing system settings, installing software, etc.
   - Prioritize tasks based on user requests or what is necessary for the task at hand. You can stretch the rules if it's essential for completing a task.

6. HANDLING ERRORS AND OUTPUTS:
   - If a command results in an error or a permission issue, inform the user immediately.
   - If a command usually doesn't produce an output, assume it executed successfully unless proven otherwise. If an output is expected but not produced, inform the user and suggest potential solutions.

7. LIMITATIONS ON REPEATING COMMANDS:
   - Avoid running the same command more than twice.
   - If a command doesn't work after two attempts, advise the user to try it manually or offer alternative solutions.

Note: In cases where a command might take a long time to execute, like installnig something via pip, execute it and ask the user for confirmation before proceeding. Suggest waiting for about 10 seconds before continuing.
"""

conversation_history_file = "/Users/anthonyh/MagicTerminal/conversation_history.json"

def get_system_info():
    current_path = os.getcwd()
    return {
        "current_path": current_path
    }
    
# Define the tool array
tools = [
    {
        "type": "function",
        "function": {
            "name": "run_command",
            "description": f"Execute a specified command line command in Zsh on macOS. Commands run after the user responds to you agian. Current path: {get_system_info()['current_path']}",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The command line command to execute, it should JUST be the command, nothing else. Make sure it's a valid command."
                    }
                },
                "required": ["command"]
            }
        }
    }
    # Additional tools can be defined here
]

def load_conversation_history():
    if os.path.exists(conversation_history_file):
        with open(conversation_history_file, "r") as file:
            return json.load(file)
    return [{"role": "system", "content": system_prompt}]

def save_conversation_history(history):
    with open(conversation_history_file, "w") as file:
        json.dump(history, file, indent=4)

def delete_conversation_history():
    if os.path.exists(conversation_history_file):
        os.remove(conversation_history_file)

def run_command(command):
    """Write the command to a file for execution and read its output from another file."""
    command_file = '/Users/anthonyh/MagicTerminal/command_to_run.txt'
    output_file = '/Users/anthonyh/MagicTerminal/command_output.txt'
    print(f"\033[90mRunning command: {command}\033[0m")

    try:
        # Write the command to a file
        with open(command_file, 'w') as file:
            file.write(command)

        # Wait for a longer period to allow the command to execute
        time.sleep(1.35)  # Adjust this time based on expected command execution time

        # Check if the output file exists before trying to read from it
        if os.path.exists(output_file):
            with open(output_file, 'r') as file:
                output = file.read().strip()
        else:
            output = "output not found."
    except Exception as e:
        output = f"An error occurred: {e}"

    formatted_output = f"Command that was executed: {command} - Command Output: {output}"

    # Delete the output file after all processing is done
    if os.path.exists(output_file):
        os.remove(output_file)

    return json.dumps({"output": formatted_output})

def display_timeout_message():
    print("[Miles is taking longer than expected...]")

def handle_tool_calls(tool_calls, conversation_history, available_functions):
    for tool_call in tool_calls:
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)
        function_to_call = available_functions.get(function_name)

        if function_to_call:
            function_response = function_to_call(**function_args)
            conversation_history.append({
                "tool_call_id": tool_call.id,
                "role": "function",
                "name": function_name,
                "content": function_response,
            })

def ask(question, conversation_history):
    if question.lower() == "delete history":
        delete_conversation_history()
        # Clear the terminal screen
        os.system('clear')
        return "\033[90mConversation history deleted and terminal cleared.\033[0m"

    conversation_history.append({"role": "user", "content": question})

    # Define available functions here
    available_functions = {
        "run_command": run_command,
        # Add other available functions here
    }

    response = None
    while True:
        # Interaction with the model
        response = client.chat.completions.create(
            model=current_model,
            messages=conversation_history,
            tools=tools,
            tool_choice="auto",
        )

        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        if not tool_calls:
            break

        handle_tool_calls(tool_calls, conversation_history, available_functions)

    # Final processing after all tool calls are handled
    final_response_message = response.choices[0].message.content if response else ""
    conversation_history.append({"role": "assistant", "content": final_response_message})

    save_conversation_history(conversation_history)
    return final_response_message

last_interaction_file = "last_interaction.txt"

def save_last_interaction_time():
    with open(last_interaction_file, "w") as file:
        file.write(datetime.datetime.now().isoformat())

def get_last_interaction_time():
    if os.path.exists(last_interaction_file):
        with open(last_interaction_file, "r") as file:
            return datetime.datetime.fromisoformat(file.read().strip())
    return None

def main():
    if len(sys.argv) > 1:
        last_interaction_time = get_last_interaction_time()
        current_time = datetime.datetime.now()

        if last_interaction_time and (current_time - last_interaction_time).total_seconds() > 1500:
            delete_conversation_history()

        user_input = " ".join(sys.argv[1:])
        conversation_history = load_conversation_history()
        response = ask(user_input, conversation_history)
        print(f"\033[1mMiles ~\033[0m {response}")

        save_last_interaction_time()
    else:
        print("Please provide a query.")

if __name__ == "__main__":
    main()
