#!/usr/bin/env python3
"""
Aura Programming Language - Main Entry Point
Allows execution either via direct file argument:
    aura <fichier.aura>
    python main.py <fichier.aura>
Or via CLI subcommand:
    aura run <fichier.aura>
    aura test
    aura repl
    aura vm <fichier.aura>
"""

import sys
import os

AURA_ROOT = os.path.dirname(os.path.abspath(__file__))
if AURA_ROOT not in sys.path:
    sys.path.insert(0, AURA_ROOT)

try:
    from aura.cli import main
except ImportError:
    import cli
    main = cli.main

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1].endswith(".aura"):
        target_file = sys.argv[1]
        if not os.path.exists(target_file):
            alt_path = os.path.join(AURA_ROOT, target_file)
            if os.path.exists(alt_path):
                target_file = alt_path

        if os.path.exists(target_file):
            try:
                from aura.interpreter import Interpreter
            except ImportError:
                from interpreter import Interpreter
            print(f"⚡ [Aura Engine] Exécution de : {target_file}\n")
            with open(target_file, "r", encoding="utf-8") as f:
                code = f.read()
            interp = Interpreter(working_dir=os.path.dirname(target_file) or ".")
            interp.run(code)
            sys.exit(0)
    main()
