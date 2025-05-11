Run, Notepad
WinWaitActive, Untitled - Notepad
Send, % RandomString(10)
; Save the file as .bat
Send, ^s
WinWaitActive, Save As
Send, test.bat
Send, {Enter}

; Function to generate random string
RandomString(length) {
    characters := "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    Random, rand, 1, StrLen(characters)
    result := ""
    Loop, %length%
    {
        Random, rand, 1, StrLen(characters)
        result .= SubStr(characters, rand, 1)
    }
    return result
}