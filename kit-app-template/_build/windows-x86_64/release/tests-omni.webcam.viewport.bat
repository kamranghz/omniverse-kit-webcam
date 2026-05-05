@echo off
setlocal
call "%~dp0kit\kit.exe"  --enable omni.kit.test --enable omni.kit.loop-default --/app/enableStdoutOutput=0 --/exts/omni.kit.test/testExts/0='omni.webcam.viewport' --ext-folder "%~dp0/exts"  --ext-folder "%~dp0/extscache"  --ext-folder "%~dp0/apps"  --/exts/omni.kit.test/testExtOutputPath="%~dp0/../../../_testoutput"  --portable-root "%~dp0/"  --/telemetry/mode=test --/crashreporter/data/testName="ext-test-omni.webcam.viewport" %*
