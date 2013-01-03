#!/bin/bash

./clean.sh

if [ ! -d ".git" ]; then
    git init
    git remote add origin git@github.com:embatbr/genome.git
fi

git add README TODO update_git.sh "exec.sh" clean.sh .gitignore src/*.py files/*.genome
git commit -m "$1"
git push origin master
echo "update complete"