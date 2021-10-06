# Pre-requirement

python3

see https://www.python.org/downloads/

git

see https://github.com/git-guides/install-git

# Install

## Clone repo
git clone https://github.com/IL55/api-adapter.git

## Credentials
i.e. copy file secrets.py.example to secrets.py and define all credentials

## Create python virtual env
`python3 -m venv venv`

## Activate python virtual environment
`source venv/bin/activate`

## Install dependent libs
`pip install -r requirements.txt`

# Run application from console
`python console_function.py 166651740`

# Deploy to AWS lambda

## Create zip
`deploy.zsh`

## Upload zip to lambda
https://aws.amazon.com/lambda/



