@echo off

Echo Hello, this is the installation for the Test Stand Diagnostics software.
pause

::This downloads and installs python
::Echo Installing python.
::powershell -Command "(New-Object Net.WebClient).DownloadFile('https://www.python.org/ftp/python/3.5.1/python-3.5.1.exe', 'python-3.5.1.exe')" 
::start python-3.5.1.exe
::pause

::This installs the wincom32 application so that python can talk with Microsoft Office
Echo Installing dependencies.
start pywin32-220.win32-py3.5.exe

Echo Installation complete. Navigate to the dist folder and run TSD.exe
timeout 120

::Happy to see Bosch here and to see the start of the fostering of an important relationship between CofC and Bosch.