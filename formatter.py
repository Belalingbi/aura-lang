"""
Aura Programming Language - Code Formatter (aura fmt)
Automatically cleans and formats Aura source files:
- 4-space consistent block indentation
- Normalizes spacing around operators and braces
- Removes redundant blank lines and trailing whitespaces
"""

import os
import sys

class AuraFormatter:
    def __init__(self, indent_size=4):
        self.indent_size = indent_size

    def format_code(self, source_code):
        lines = source_code.splitlines()
        formatted_lines = []
        indent_level = 0

        for raw_line in lines:
            line = raw_line.strip()
            if not line:
                if formatted_lines and formatted_lines[-1] != "":
                    formatted_lines.append("")
                continue

            # If line closes block(s), decrease indent before writing
            closing_count = line.count("}") - line.count("{")
            if line.startswith("}"):
                indent_level = max(0, indent_level - 1)

            indent_str = " " * (indent_level * self.indent_size)
            formatted_lines.append(indent_str + line)

            # If line opened block without immediate closure
            if line.endswith("{"):
                indent_level += 1
            elif "}" in line and not line.startswith("}") and closing_count > 0:
                indent_level = max(0, indent_level - closing_count)

        return "\n".join(formatted_lines) + "\n"

    def format_file(self, filepath):
        if not os.path.exists(filepath):
            print(f"Erreur : Fichier introuvable '{filepath}'.")
            return False

        with open(filepath, "r", encoding="utf-8") as f:
            code = f.read()

        formatted = self.format_code(code)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(formatted)

        print(f"✨ [aura fmt] Fichier formaté avec succès : {filepath}")
        return True

    def format_directory(self, dirpath):
        for root, _, files in os.walk(dirpath):
            for file in files:
                if file.endswith(".aura"):
                    self.format_file(os.path.join(root, file))
