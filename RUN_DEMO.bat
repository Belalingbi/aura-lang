@echo off
cd /d "%~dp0"
title Runtime Aura Language
echo =====================================================
echo   EXECUTION DU PROJET AURA (Language Universel)
echo =====================================================
echo.
echo [1/3] Execution de main.aura...
python main.py main.aura
echo.
echo [2/3] Execution de la suite globale test_global.aura...
python main.py test_global.aura
echo.
echo [3/3] Execution de la Machine Virtuelle (Bytecode VM)...
python cli.py vm programme_vm.aura
echo.
echo =====================================================
echo   TOUTES LES EXECUTIONS SONT TERMINEES AVEC SUCCES !
echo =====================================================
echo.
pause
