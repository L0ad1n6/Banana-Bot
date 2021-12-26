# Banana Bot

[![Run on Repl.it](https://repl.it/badge/github/L0ad1n6/Banana-Bot)](https://repl.it/github/L0ad1n6/Banana-Bot)

This is a general purpose bot designed for The People's Republic of Banana. In
addition to the standard moderation featues most discord bots have, Banana Bot
analyzes messages and updated users social credit on the server. Manula
intervention can be done by admins but the bot will automatically punish and
pardon people in sepcific cases. More commands will be added to the utility
file. The bot is deployed on heroku.com

## Setup

Development:

```
python -m venv ./venv
source ./venv/bin/activate
pip install -r requirements.txt
npm install nodemon
nodemon --exec python src/main.py
```

Production:

```
python -m venv ./venv
source ./venv/bin/activate
pip install -r requirements.txt
python src/main.py
```

## Usage

Type the characters "--" and then any command to run the command. Type "--help"
for help.

## Examples

```
--cred sub 100 @ELMTN
--ban @ELMTN Example usage of ban command
```
