@echo off
title Installation d'Aura dans le PATH Windows
echo =====================================================
echo   INSTALLATION D'AURA DANS LE PATH WINDOWS
echo =====================================================
echo.
powershell -Command "[Environment]::SetEnvironmentVariable('Path', [Environment]::GetEnvironmentVariable('Path', 'User') + ';%~dp0', 'User')"
echo.
echo [OK] Le dossier d'Aura a ete ajoute a votre PATH utilisateur avec succes !
echo.
echo Vous pouvez maintenant ouvrir un NOUVEAU terminal PowerShell ou CMD
echo (depuis n'importe quel dossier, y compris C:\windows\system32)
echo et taper directement :
echo.
echo    aura main.aura
echo    aura test_global.aura
echo    aura vm programme_vm.aura
echo    aura test
echo    aura repl
echo.
echo =====================================================
pause
