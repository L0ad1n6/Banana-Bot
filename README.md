# Banana Bot

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
Type the characters "--" and then any command to run the command. Type "--help" for help.

## Examples
```Discord
--ban @ELMTN Example ban
```