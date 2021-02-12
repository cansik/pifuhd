@echo off

SET RESOLUTION=512
SET LOCATION=sample_images

if not "%1"=="" (set RESOLUTION=%1)
if not "%2"=="" (set LOCATION=%2)

echo running pifu (%RESOLUTION%)...
python -m apps.simple_test -r %RESOLUTION% -i %LOCATION%