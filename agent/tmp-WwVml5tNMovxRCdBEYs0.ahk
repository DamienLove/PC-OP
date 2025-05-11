Run, notepad.exe
WinWaitActive, Untitled - Notepad
Send, {Random 10} ; Send 10 random characters
Send, ^s ; Ctrl+S to save
WinWaitActive, Save As
Send, c:\users\satan\test.bat{Enter}