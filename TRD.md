# Technical Requirements Document (TRD) — Architecture & Sécurité d'Aura

- **Version :** 1.0
- **Langage hôte :** Python 3.x (bibliothèque standard + `pygls` optionnel pour le LSP)
- **Composants principaux :** Lexer, Parser/AST, Interpréteur AST, Compilateur Bytecode & VM à pile + GC, Transpileur C (AOT), Pont FFI, Moteur de concurrence CSP, CLI/REPL/Outils.

---

## 1. Architecture Globale et Pipelines d'Exécution

Aura repose sur deux moteurs d'exécution partageant le front-end lexical et syntaxique :

```text
Source (.aura / REPL)
       │
       ▼
  [ Lexer ] ──► Flux de Tokens (type, valeur, ligne/colonne)
       │
       ▼
  [ Parser ] ──► Arbre Syntaxique Abstrait (AST)
       │
       ├──► Voie A (Interpréteur / REPL) : Évaluation directe via visiteur d'AST + Environment
       │
       ├──► Voie B (Bytecode VM) : Compiler ──► Chunk (Opcodes + Constantes) ──► VirtualMachine + GC
       │
       └──► Voie C (Compilation AOT) : AuraNativeCompiler ──► Code C ──► gcc -O3 ──► Binaire natif