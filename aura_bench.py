"""
Aura Programming Language - Benchmark Tool (aura bench)
Runs microbenchmarks and stress tests on Aura scripts.
"""

import time
import os
import sys
from interpreter import Interpreter

class AuraBench:
    def __init__(self, iterations=10):
        self.iterations = iterations

    def benchmark_file(self, filepath):
        if not os.path.exists(filepath):
            print(f"Erreur : Fichier '{filepath}' introuvable.")
            return

        with open(filepath, "r", encoding="utf-8") as f:
            code = f.read()

        print(f"🔥 [Aura Bench] Lancement du benchmark pour '{filepath}' ({self.iterations} itérations)...")
        durations = []

        for i in range(self.iterations):
            interp = Interpreter(working_dir=os.path.dirname(filepath) or ".")
            start = time.perf_counter()
            interp.run(code)
            elapsed = (time.perf_counter() - start) * 1000.0
            durations.append(elapsed)

        avg = sum(durations) / len(durations)
        best = min(durations)
        worst = max(durations)

        print("\n-----------------------------------------------------")
        print(f"📊 Résultats du Benchmark : {filepath}")
        print(f"   Itérations : {self.iterations}")
        print(f"   Temps Moyen: {avg:.2f} ms")
        print(f"   Meilleur   : {best:.2f} ms")
        print(f"   Plus Lent  : {worst:.2f} ms")
        print("-----------------------------------------------------")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        bench = AuraBench()
        bench.benchmark_file(sys.argv[1])
    else:
        print("Usage : python aura_bench.py <fichier.aura>")
