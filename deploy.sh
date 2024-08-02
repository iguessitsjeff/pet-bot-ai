#!/bin/bash
set -exu

# Get SSO token before running AWS Commands

pipenv requirements > requirements.txt

sam build

## Inspect local invoke and make sure the lambda passed.
echo
read -p "Continue Script? [N]" -n 1 -r
echo    # (optional) move to a new line
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    exit 1
fi

# Deploy if y/Y is entered
sam deploy --guided