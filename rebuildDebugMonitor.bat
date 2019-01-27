@echo off
cd /d %~dp0
call "D:\Program Files\Microsoft Visual Studio\2017\Community\Common7\Tools\VsDevCmd.bat"
devenv.exe testRun.sln /Rebuild "Debug|x86"
