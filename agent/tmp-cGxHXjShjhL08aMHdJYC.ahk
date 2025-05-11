Run, Notepad
WinWaitActive, Untitled - Notepad
Send, {Blind} % RandomChar(10) 
Send, ^s
WinWaitActive, Save As
Send, %A_Desktop%\test.baty{Enter}
return

RandomChar(count) {
    chars := "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    Random, rand, 1, % StrLen(chars)
    ; build the random string
    str := ""
    Loop, %count% {
        Random, rand, 1, % StrLen(chars)
        str .= SubStr(chars, rand, 1)
    }
    return str
}