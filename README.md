# SamuraiQuest

SamuraiQuest is a Discord bot created for the CoderDojo Braga community. Its purpose is to simplify member onboarding, manage challenge submissions, and handle role assignments based on user reactions. SamuraiQuest helps to keep the server organized and enhances interaction between mentors and ninjas.

## Features

- **Welcome Message**: Automatically welcomes new members and guides them through initial steps on the server.
- **Role Assignment**: Allows members to select roles based on the type of challenges they prefer, like Scratch or Python.
- **Challenge Management**: Processes challenge submissions in Scratch and Python, updating a status message to track participant progress.
- **Emoji Reactions**: Adds and removes roles based on users' reactions to specific messages.
- **Rank Management**: Allows mentors to promote ninjas by assigning roles for achieved ranks.

## Installation

1. Clone this repository:
    
    ```bash
    git clone git@github.com:coderdojobraga/SamuraiQuest.git
    cd SamuraiQuest
    ```
    
2. Install required dependencies:
    
    ```bash
    pip install -r requirements.txt
    ```
    
3. Create a `.env` file in the project root and add your Discord token:
    
    ```
    DISCORD_TOKEN=your_discord_token
    ```
    
4. Configure the channel, message, and role IDs in `main.py` according to the CoderDojo Braga Discord server.

## Usage

To start the bot, run:

```bash
python3 src/main.py
```

SamuraiQuest will now be ready to interact with server members and automatically handle its assigned functions.

## Code Structure

- **main.py**: Main file containing bot configuration and event handling logic.
- **utils.py**: Helper functions for message updates and pattern checks in submissions.

## Configuring Roles and Channels

In `main.py`, there are dictionaries for configuring the specific IDs for the CoderDojo Braga server’s channels and roles:

- **channel_ids**: Defines IDs for each channel the bot uses.
- **message_ids**: Contains IDs for key messages that the bot will monitor and update.
- **react_roles**: Defines emojis and their corresponding roles for user assignment.

## Contribution

Contributions are welcome! Feel free to open an issue or submit a pull request with improvements.

## License

This project is licensed under the **MIT License**.

---

We hope **SamuraiQuest** enriches the CoderDojo Braga community experience! 🚀