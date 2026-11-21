#!/usr/bin/env python3
"""
Aura Programming Language - CLI Launcher
"""
import sys
import os

AURA_ROOT = os.path.dirname(os.path.abspath(__file__))
if AURA_ROOT not in sys.path:
    sys.path.insert(0, AURA_ROOT)

from aura.cli import main

if __name__ == "__main__":
    main()
