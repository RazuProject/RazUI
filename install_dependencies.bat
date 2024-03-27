@echo off

:ask

echo.
echo  Is PIP added to path? (Y/N)
echo.
set /p input= : 

goto %input%
goto ask

:y
:Y

echo.
echo Dependencies will now be installed
pip install -r dependencies.txt
echo \_____ Done!

pause

goto n

:n
:N

exit