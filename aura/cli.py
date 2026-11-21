#!/usr/bin/env python3
"""
Aura Programming Language - Official Command Line Interface (CLI)
Usage:
    aura run [fichier.aura]
    aura repl
    aura test
    aura new <nom_du_projet>
    aura fmt [fichier_ou_dossier]
    aura doc [fichier_ou_dossier]
    aura bench [fichier.aura]
    aura vm [fichier.aura]
"""

import sys
import os
import argparse
import json
try:
    from .lexer import Lexer
    from .parser import Parser
    from .interpreter import Interpreter, Environment, AuraUserException, AuraRuntimeError
    from .compiler import Compiler
    from .vm import VirtualMachine
    from .formatter import AuraFormatter
    from .doc_generator import AuraDocGenerator
    from .aura_test import AuraTestRunner
    from .aura_bench import AuraBench
except (ImportError, ValueError):
    from lexer import Lexer
    from parser import Parser
    from interpreter import Interpreter, Environment, AuraUserException, AuraRuntimeError
    from compiler import Compiler
    from vm import VirtualMachine
    from formatter import AuraFormatter
    from doc_generator import AuraDocGenerator
    from aura_test import AuraTestRunner
    from aura_bench import AuraBench

BANNER = r"""
       /\
      /  \        A U R A   L A N G U A G E
     / /\ \       Version 1.0.0
    / ____ \      Dynamic, Secure & Concurrent Programming
   /_/    \_\
"""

def cmd_new(args):
    project_name = args.name
    print(f"🚀 Initialisation du nouveau projet Aura : '{project_name}'...")
    if os.path.exists(project_name):
        print(f"Erreur : Le dossier '{project_name}' existe déjà.")
        sys.exit(1)

    os.makedirs(project_name)
    tests_dir = os.path.join(project_name, "tests")
    os.makedirs(tests_dir)

    # aura.json
    config = {
        "name": project_name,
        "version": "1.0.0",
        "description": f"Projet développé en langage Aura : {project_name}",
        "main": "main.aura"
    }
    with open(os.path.join(project_name, "aura.json"), "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    # main.aura
    main_code = f"""// Point d'entrée principal pour {project_name}

print("🌟 Bienvenue dans votre application Aura !")

fn saluer(nom) {{
    return f"Bonjour {{nom}}, bienvenue dans Aura !"
}}

print(saluer("Développeur"))
"""
    with open(os.path.join(project_name, "main.aura"), "w", encoding="utf-8") as f:
        f.write(main_code)

    # test_principal.aura
    test_code = f"""// Tests unitaires pour {project_name}

print("🧪 Exécution des tests du projet...")
assert(1 + 1 == 2, "Test arithmétique de base")
assert("Aura".len() == 4, "Longueur de chaîne valide")
print("✅ Tous les tests sont validés avec succès !")
"""
    with open(os.path.join(tests_dir, "test_principal.aura"), "w", encoding="utf-8") as f:
        f.write(test_code)

    print(f"✨ Projet '{project_name}' initialisé avec succès !")
    print(f"   Tapez 'cd {project_name}' puis 'python ../cli.py run' pour lancer votre code.")

def resolve_aura_file(filepath):
    if not filepath:
        return None
    if os.path.exists(filepath):
        return os.path.abspath(filepath)
    cli_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(cli_dir, filepath),
        os.path.join(os.path.dirname(cli_dir), filepath),
        os.path.join(r"C:\Users\belal\Downloads\AURA", filepath),
    ]
    for cand in candidates:
        if os.path.exists(cand):
            return os.path.abspath(cand)
    return None

def cmd_run(args):
    filepath = args.file
    if not filepath:
        if os.path.exists("aura.json"):
            try:
                with open("aura.json", "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                filepath = cfg.get("main", "main.aura")
            except Exception:
                filepath = "main.aura"
        else:
            filepath = "main.aura"

    resolved = resolve_aura_file(filepath)
    if not resolved:
        print(f"Erreur : Fichier source '{filepath}' introuvable.")
        sys.exit(1)
    filepath = resolved

    print(f"⚡ [Aura Engine] Exécution du fichier : {filepath}\n")
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            code = f.read()
        interp = Interpreter(working_dir=os.path.dirname(filepath) or ".")
        interp.run(code)
    except AuraUserException as e:
        print(f"\n💥 [Exception Aura Non Interceptée] : {e}")
        sys.exit(1)
    except AuraRuntimeError as e:
        print(f"\n💥 [Erreur d'Exécution] : {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 [Erreur Inattendue] : {e}")
        sys.exit(1)

def cmd_vm(args):
    filepath = args.file
    if not filepath:
        filepath = "main.aura"
    resolved = resolve_aura_file(filepath)
    if not resolved:
        print(f"Erreur : Fichier source '{filepath}' introuvable.")
        sys.exit(1)
    filepath = resolved

    print(f"⚡ [Aura Bytecode VM] Compilation et exécution de : {filepath}\n")
    with open(filepath, "r", encoding="utf-8") as f:
        code = f.read()

    lexer = Lexer(code)
    parser = Parser(lexer)
    ast = parser.parse()

    compiler = Compiler()
    chunk = compiler.compile(ast)

    vm = VirtualMachine(chunk)
    vm.run()
    print("\n✔ Exécution terminée par la machine virtuelle Aura !")

def cmd_repl(args):
    print(BANNER)
    print("Mode REPL interactif activé. Tapez 'exit' ou 'quit' pour quitter.\n")
    interp = Interpreter()
    repl_env = interp.global_env

    while True:
        try:
            line = input("aura> ")
            if line.strip() in ("exit", "quit", "exit()", "quit()"):
                print("Fermeture du REPL Aura. À bientôt !")
                break
            if not line.strip():
                continue

            # If user entered an expression, wrap in print if needed, or evaluate
            try:
                res = interp.run(line, env=repl_env)
                if res is not None:
                    print(res)
            except Exception as e:
                print(f"Erreur : {e}")
        except (KeyboardInterrupt, EOFError):
            print("\nFermeture du REPL.")
            break

def cmd_test(args):
    test_dir = args.dir if hasattr(args, "dir") and args.dir else "tests"
    runner = AuraTestRunner(test_dir=test_dir)
    success = runner.run_all()
    if not success:
        sys.exit(1)

def cmd_fmt(args):
    target = args.path if args.path else "."
    formatter = AuraFormatter()
    if os.path.isfile(target):
        formatter.format_file(target)
    else:
        formatter.format_directory(target)

def cmd_doc(args):
    target = args.path if args.path else "."
    generator = AuraDocGenerator()
    generator.generate(target)

def cmd_bench(args):
    filepath = args.file if args.file else "main.aura"
    iterations = args.iterations if hasattr(args, "iterations") and args.iterations else 10
    bench = AuraBench(iterations=iterations)
    bench.benchmark_file(filepath)

def main():
    parser = argparse.ArgumentParser(
        description="CLI officielle du langage de programmation Aura 🌟",
        prog="aura"
    )
    subparsers = parser.add_subparsers(dest="command", help="Commandes disponibles")

    # run
    p_run = subparsers.add_parser("run", help="Exécute un script Aura via l'interpréteur AST")
    p_run.add_argument("file", nargs="?", type=str, help="Fichier .aura à exécuter (défaut : main.aura)")
    p_run.set_defaults(func=cmd_run)

    # repl
    p_repl = subparsers.add_parser("repl", help="Lance la boucle interactive REPL")
    p_repl.set_defaults(func=cmd_repl)

    # vm
    p_vm = subparsers.add_parser("vm", help="Compile et exécute via la VM Bytecode Aura + GC")
    p_vm.add_argument("file", nargs="?", type=str, help="Fichier .aura à compiler")
    p_vm.set_defaults(func=cmd_vm)

    # test
    p_test = subparsers.add_parser("test", help="Exécute la suite de tests unitaires")
    p_test.add_argument("--dir", type=str, default="tests", help="Répertoire de tests")
    p_test.set_defaults(func=cmd_test)

    # new
    p_new = subparsers.add_parser("new", help="Initialise une structure de projet Aura")
    p_new.add_argument("name", type=str, help="Nom du nouveau projet")
    p_new.set_defaults(func=cmd_new)

    # fmt
    p_fmt = subparsers.add_parser("fmt", help="Formate automatiquement les fichiers source")
    p_fmt.add_argument("path", nargs="?", type=str, default=".", help="Fichier ou répertoire")
    p_fmt.set_defaults(func=cmd_fmt)

    # doc
    p_doc = subparsers.add_parser("doc", help="Génère la documentation Markdown du code source")
    p_doc.add_argument("path", nargs="?", type=str, default=".", help="Fichier ou répertoire")
    p_doc.set_defaults(func=cmd_doc)

    # bench
    p_bench = subparsers.add_parser("bench", help="Mesure les performances d'un script Aura")
    p_bench.add_argument("file", nargs="?", type=str, default="main.aura", help="Fichier .aura")
    p_bench.add_argument("-n", "--iterations", type=int, default=10, help="Nombre d'itérations")
    p_bench.set_defaults(func=cmd_bench)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        # Default behavior: run main.aura if exists, else repl
        if os.path.exists("main.aura") or os.path.exists("aura.json"):
            args.file = None
            cmd_run(args)
        else:
            parser.print_help()

if __name__ == "__main__":
    main()
