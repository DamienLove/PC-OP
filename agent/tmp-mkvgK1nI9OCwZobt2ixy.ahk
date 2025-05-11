Run, Notepad
WinWait, Untitled - Notepad
Send, % RandomString(10)

RandomString(length) {
    chars := "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    String := ""
    Loop, %length%
    {
        Random, index, 1, StrLen(chars)
        String .= SubStr(chars, index, 1)
    }
    return String
}