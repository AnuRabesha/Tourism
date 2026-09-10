@echo off
set GIT="C:\Program Files\Git\bin\git.exe"

echo [0/7] Setting git user config...
%GIT% config --global user.email "anurabesha07@gmail.com"
%GIT% config --global user.name "Anu Rabesha.A"

echo [1/7] Initializing git repo...
%GIT% init

echo [2/7] Adding all files...
%GIT% add .

echo [3/7] Committing...
%GIT% commit -m "first commit"

echo [4/7] Setting branch to main...
%GIT% branch -M main

echo [5/7] Adding remote origin...
%GIT% remote remove origin 2>nul
%GIT% remote add origin https://github.com/AnuRabesha/Tourism.git

echo [6/7] Pushing to GitHub...
%GIT% push -u origin main

echo.
echo Done! Visit https://github.com/AnuRabesha/Tourism
pause
