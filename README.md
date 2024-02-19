# MagicTerminal 🌐🖥️

MagicTerminal is an innovative command-line interface that leverages the advanced AI capabilities of [M.I.L.E.S](https://github.com/small-cactus/M.I.L.E.S), integrating OpenAI's GPT-4-Turbo model for natural language processing. This allows users to interact with their terminal using natural language, making command line tasks more intuitive and accessible.

## About MagicTerminal

MagicTerminal is designed to understand and execute a wide range of commands in a conversational manner. By harnessing the power of the M.I.L.E.S AI, it provides an intuitive way to navigate and perform tasks within your terminal without needing to remember specific command syntax.

## Key Features

- AI Command Interpretation: Converts natural language inputs into command line instructions.
- Multi-Command Capability: Can process and execute up to three commands simultaneously.
- Broad Functionality: Equipped to handle diverse tasks, from file searches to answering general questions.

## How It Works

1. Activation: Use the wake word `miles` to activate the AI within your terminal.
2. Input Command: Simply type your command or question in natural language.
3. Execution: MagicTerminal interprets your input and executes the command, providing immediate and accurate responses.

### Example Interactions

```
miles who invented the lightbulb
# Response: "Thomas Edison is typically credited with inventing the lightbulb."

miles list all jpg files in my documents
# Response: "There are 20 jpg files in your documents folder."
```

## Installation

1. **Clone Repo**
   ```
   git clone https://github.com/small-cactus/MagicTerminal.git
   ```
   Make sure you use cd to navigate to the directory, then:

2. **Run setup script**
   ```
   chmod +x setup.sh
   ```
   ```
   ./setup.sh
   ```
3. **Hope it worked?**
   This repo is not my main focus whatsoever, if you want command line magic that feels like magic, try [Open-Interpreter](https://github.com/KillianLucas/open-interpreter)

## Usage

To use MagicTerminal, start your command with `miles`, followed by your question or command in natural language:

```
miles [your question or command]
```

For example:

```
miles find all documents containing 'budget'
# Response: "Located 3 documents with 'budget' in them. What should I do with them?"
```

## Known Issues

- **Setup Difficulties**: Some users may experience issues with the automatic setup process. If MagicTerminal does not work immediately after installation, you may need to manually edit your `.zshrc` file to add the MagicTerminal function definition.
- **Contextual Limitations**: Due to the current implementation, all commands are not appended to the AI's context until you prompt it again. This can lead to a situation where the AI provides double responses or utilizes more tokens than necessary for a single task. We are aware of this issue and are working on a solution. Users should be mindful of this in this alpha release and plan their interactions accordingly.

## Contributing

We welcome contributions to MagicTerminal. Please see our [Contributing Guidelines](LINK_TO_CONTRIBUTING_GUIDELINES) for more information on how to get involved.

## License

MagicTerminal is licensed under the MIT License. For more details, see [LICENSE](LINK_TO_LICENSE).

## Contact

If you have any questions or feedback about MagicTerminal, please reach out to us [here](LINK_TO_CONTACT_PAGE).

---

**MagicTerminal**: Redefining Command Line Intelligence with the power of M.I.L.E.S AI.
