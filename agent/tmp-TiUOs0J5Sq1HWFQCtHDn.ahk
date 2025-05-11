Run, Notepad
WinWaitActive, Untitled - Notepad
Send, {Random,10}
Send, ^s
WinWaitActive, Save As
Send, %A_Desktop%\test.baty
Send, {Enter}