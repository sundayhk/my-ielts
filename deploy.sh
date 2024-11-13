#!/bin/bash
npm run build
cd dist
git pull --rebase
git add . && git commit -m 'update dist'
git push
echo "deploy success!"
