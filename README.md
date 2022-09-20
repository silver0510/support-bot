## Setup environment
----------------------------------------------------------------
#### Create a virtual environment
    `python -m venv -path`
#### Go to the virtual environment
    `source <venv>/Scripts/activate`
#### Make `requirements.txt` file
    `pip3 freeze > requirements.txt`
#### Install libraries from requirements.txt
    `pip3 install -r requirements.txt `

## Make executable file from script:
----------------------------------------------------------------
#### Step 1 - Install library
    `pip3 install pyinstaller`
#### Step 2 - Go to the script's location
    `cd script-path`
#### Step 3 - Create the executable
    `pyinstaller -F -n 'Auto order' index.py`

## Deployment Guide
-----------------------------------------------------------------
#### [Guide Link](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Hosting-your-bot)

#### Delete screen section:
    `screen -X -S [session # you want to kill] quit`