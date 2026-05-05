@echo off
setlocal
call "%~dp0kit\kit.exe"  --ext-folder "%~dp0/exts"  --ext-folder "%~dp0/extscache"  --ext-folder "%~dp0/apps"  %*
