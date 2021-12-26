# Banana Bot

[![Run on Repl.it](https://repl.it/badge/github/L0ad1n6/Banana-Bot)](https://repl.it/github/L0ad1n6/Banana-Bot)

This is a general purpose bot designed for The People's Republic of Banana. In
addition to the standard moderation featues most discord bots have, Banana Bot
analyzes messages and updated users social credit on the server. Manula
intervention can be done by admins but the bot will automatically punish and
pardon people in sepcific cases. More commands will be added to the utility
file. The bot is deployed on heroku.com

## Table of Contents

- [Setup](#setup)
- [Details](#details)
- [Project Structure](project_structure)
- [Licence](#licence)

## Setup

- Clone Repository

```Sh
git clone https://github.com/L0ad1n6/Banana-Bot
```

- Configure Discord Token

```Sh
cd Banana-Bot
echo token=YOUR-TOKEN-HERE>.env
```

- Create Virtual Enviornment (Optional)

```Sh
python -m venv ./venv
source ./venv/bin/activate
```

- Installing Dependencies

All of the project dependencies are in the requirements.txt file

```
pip install -r requirements.txt
```

- Running Code

For development nodemon is a very powerfull tool:

```Sh
npm install nodemon
nodemon --exec python src/main.py
```

For local deployment:

```Sh
python src/main.py
```

For production I would adivse using [heroku](https://www.heroku.com)

## Usage

Type the characters "--" and then any command or command alias to run the
command. Type "--help" for a list of commands help.

```

--cred sub 100 @ELMTN --ban @ELMTN Example usage of ban command

```
