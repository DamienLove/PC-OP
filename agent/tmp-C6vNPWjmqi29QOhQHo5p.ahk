Run, Notepad
WinWaitActive, Untitled - Notepad
Send, % RandomChars(10)
Send, ^s
WinWaitActive, Save As
Send, %A_Desktop%\test.baty
Send, {Enter}
Return

RandomChars(length) {
    chars := "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    Random, randomIndex, 1, StrLen(chars)
    result := ""
    Loop, %length%
    {
        Random, randomIndex, 1, StrLen(chars)
        result .= SubStr(chars, randomIndex, 1)
    }
    return result
}