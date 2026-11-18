@echo off
setlocal
cd /d "%~dp0"

echo.
echo ================================================
echo   3RD Company website - publish to GitHub Pages
echo ================================================
echo.

git add -A
git commit -m "Update website"
if errorlevel 1 echo ^(nothing new to publish^)

git push

echo.
echo Done. The live site updates in about one minute:
echo   https://yyedediqizhang-glitch.github.io/3rd-company/
echo.
pause
