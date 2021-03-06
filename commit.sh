#!/bin/bash
#echo Stashing...
#git stash
echo Switching to master...
git checkout master
#echo Popping...
#git stash pop
echo Committing...
git commit -s$1
echo Switching back to EntiPit
git checkout EntiPit
echo Rebasing...
git rebase master EntiPit
if [[ "$2" == p* ]]
then
  echo Pushing to GitHub...
  git push github master
else
  echo Not Pushing...
fi
echo Done!
