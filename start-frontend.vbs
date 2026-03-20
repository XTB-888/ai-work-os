Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "cmd /c cd /d C:\Users\monarch\Documents\AI-Work-OS\frontend && pnpm dev", 0, False
Set WshShell = Nothing
