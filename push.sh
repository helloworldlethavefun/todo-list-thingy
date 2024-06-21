#! /bin/zsh

echo -e "What files would you like to commit? "
read commitFiles

echo -e "Commit message: "
read message

git add $commitFiles
git commit -m "$message"
git push -u origin main
