"""
Aura Programming Language - Documentation Generator (aura doc)
Parses Aura files, extracts function signatures, class declarations, and doc comments,
producing clean Markdown documentation.
"""

import os
import re

class AuraDocGenerator:
    def __init__(self, output_file="DOCS.md"):
        self.output_file = output_file

    def extract_docs_from_code(self, filename, code):
        entries = []
        lines = code.splitlines()
        last_comments = []

        for line in lines:
            trimmed = line.strip()
            if trimmed.startswith("//"):
                last_comments.append(trimmed.lstrip("/").strip())
            elif trimmed.startswith("class "):
                m = re.match(r"class\s+([A-Za-z0-9_]+)(?:\s+extends\s+([A-Za-z0-9_]+))?", trimmed)
                if m:
                    cls_name = m.group(1)
                    parent = m.group(2)
                    doc = " ".join(last_comments) if last_comments else "Aucune description fournie."
                    entries.append({
                        "type": "Classe",
                        "name": cls_name + (f" (extends {parent})" if parent else ""),
                        "doc": doc
                    })
                last_comments = []
            elif trimmed.startswith("fn "):
                m = re.match(r"fn\s+([A-Za-z0-9_]+)\s*\((.*?)\)", trimmed)
                if m:
                    fn_name = m.group(1)
                    params = m.group(2)
                    doc = " ".join(last_comments) if last_comments else "Aucune description fournie."
                    entries.append({
                        "type": "Fonction",
                        "name": f"{fn_name}({params})",
                        "doc": doc
                    })
                last_comments = []
            elif trimmed and not trimmed.startswith("@"):
                last_comments = []

        return entries

    def generate(self, target_path="."):
        all_docs = {}

        if os.path.isfile(target_path):
            files = [target_path]
        else:
            files = []
            for root, _, fs in os.walk(target_path):
                for f in fs:
                    if f.endswith(".aura"):
                        files.append(os.path.join(root, f))

        for filepath in files:
            with open(filepath, "r", encoding="utf-8") as f:
                code = f.read()
            docs = self.extract_docs_from_code(os.path.basename(filepath), code)
            if docs:
                all_docs[os.path.basename(filepath)] = docs

        # Generate markdown
        md = ["# 📖 Documentation de l'API du Projet Aura\n"]
        for fname, items in all_docs.items():
            md.append(f"## Fichier : `{fname}`\n")
            for item in items:
                md.append(f"### `[{item['type']}]` {item['name']}")
                md.append(f"> {item['doc']}\n")

        content = "\n".join(md)
        with open(self.output_file, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"📄 [aura doc] Documentation générée avec succès dans '{self.output_file}' ({len(files)} fichier(s) analysé(s)).")
        return self.output_file
