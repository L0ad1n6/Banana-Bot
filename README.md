# Banana Bot

[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)
[![Run on Repl.it](https://repl.it/badge/github/L0ad1n6/Banana-Bot)](https://repl.it/github/L0ad1n6/Banana-Bot)

Banana Bot is a bot designed for The People's Republic of Banana. In addition to
the moderation and utility commands standard in most bots, Banana Bot analyzes
messages sent and determines whether a message is "againt the state", "neutral"
or "praising the state". Depending on the verdict of the model the members
social credit is adjusted. Manual intervention can be done by admins, however,
bot will take care of punishements and pardons automatically with respect to
social credit. I plan to add more utility commands in the future.

## Table of Contents

- [Setup](#setup)
- [Usage](#usage)
- [Project Structure](project_structure)
- [Licence](#licence)

### Setup

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

### Usage

Type the characters "--" and then any command or command alias to run the
command. Type "--help" for a list of commands help.

#### Examples

![Credit Command](https://github.com/L0ad1n6/Banana-Bot/blob/main/src/data/photos/cred.png?raw=true)
![Credit Command](https://github.com/L0ad1n6/Banana-Bot/blob/main/src/data/photos/help.png?raw=true)
![Credit Command](https://github.com/L0ad1n6/Banana-Bot/blob/main/src/data/photos/ban.png?raw=true)

### Project Structure

| Name                 | Description                                                                |
| -------------------- | -------------------------------------------------------------------------- |
| **requirements.txt** | Has all of the package requirements                                        |
| **Procfile**         | Config file for [heroku](https://www.heroku.com)                           |
| **LICENSE**          | Holds license for bot                                                      |
| **.gitignore**       | Standard gitignore file to prevent unwanted files form being commited      |
| **.prettierrc**      | Config file for prettier                                                   |
| **src**              | Contains all source code for project                                       |
| **src/commands**     | All commmand related code is found in this dirrectory                      |
| **src/data**         | Data such as member data, photos, dataset and ml model are stored here     |
| **src/model**        | All code related to training the model are located in this dirrectory      |
| **src/main**         | Entrypoint to the code, pieces together all the different parts of the bot |

### Licence

Licenced under the [MIT](LICENSE) License

Copyright (c) 2021 Altan Mehmet Ünver (L0ad1n6)

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
