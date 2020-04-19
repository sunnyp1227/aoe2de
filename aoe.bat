@echo off
set STEAM_ID=76561198001071301

:: List of supported languages: 
:: en, de, el, es, es-MX, fr, hi, it, ja, ko, ms, nl, pt, ru, tr, vi, zh, zh-TW
set LANGUAGE=en

python aoe.py %STEAM_ID% %LANGUAGE%
