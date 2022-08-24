::git init
git add .

git commit -m "first commit"
::heroku git:remote -a tele2442
git push heroku master

pause