Run, notepad.exe
WinWaitActive, Untitled - Notepad
Send, % RandomString(10)
Send, ^s
Sleep, 100
Send, %A_Desktop%\test.baty
Send, {Enter}
WinClose, Untitled - Notepad

RandomString(length) {
    characters := "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    randomString := ""
    Loop, %length%
    {
        Random, randIndex, 1, StrLen(characters)
        randomString .= SubStr(characters, randIndex, 1)
    }
    return randomString
}