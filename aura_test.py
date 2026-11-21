"""
Aura Programming Language - Test Framework (aura test)
Provides assertion utilities and test runners for executing Aura test suites.
"""

import os
import sys
import time
from interpreter import Interpreter, AuraUserException, AuraRuntimeError

class AuraAssertions:
    @staticmethod
    def assert_eq(actual, expected, message=""):
        if actual != expected:
            raise AssertionError(f"Attendu '{expected}', mais obtenu '{actual}'. {message}")

    @staticmethod
    def assert_true(condition, message=""):
        if not bool(condition):
            raise AssertionError(f"La condition évaluée est fausse. {message}")

    @staticmethod
    def assert_false(condition, message=""):
        if bool(condition):
            raise AssertionError(f"La condition évaluée est vraie alors qu'elle était attendue fausse. {message}")

class AuraTestRunner:
    def __init__(self, test_dir="tests"):
        self.test_dir = test_dir
        self.tests = []

    def register_python_test(self, name, test_func):
        self.tests.append((name, test_func, "py"))

    def find_aura_tests(self):
        found = []
        if os.path.exists(self.test_dir):
            for root, _, files in os.walk(self.test_dir):
                for f in files:
                    if f.endswith(".aura"):
                        found.append(os.path.join(root, f))
        return sorted(found)

    def run_aura_file(self, filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            code = f.read()
        interp = Interpreter(working_dir=os.path.dirname(filepath) or ".")
        interp.run(code)

    def run_all(self):
        print("🧪 [Aura Test] Recherche et exécution de la suite de tests unitaires...")
        
        aura_files = self.find_aura_tests()
        total = len(self.tests) + len(aura_files)
        
        if total == 0:
            print("Aucun fichier de test trouvé.")
            return True

        print(f"🚀 [Aura Test] Lancement de {total} cible(s) de test...\n")
        passed = 0
        failed = 0

        # Run registered python tests
        for name, func, _ in self.tests:
            start = time.perf_counter()
            try:
                func()
                elapsed = (time.perf_counter() - start) * 1000
                print(f"  ✅ PASS [{elapsed:.2f}ms] : {name}")
                passed += 1
            except Exception as e:
                elapsed = (time.perf_counter() - start) * 1000
                print(f"  ❌ FAIL [{elapsed:.2f}ms] : {name}")
                print(f"     ↳ {e}")
                failed += 1

        # Run .aura test files
        for test_file in aura_files:
            start = time.perf_counter()
            try:
                self.run_aura_file(test_file)
                elapsed = (time.perf_counter() - start) * 1000
                print(f"  ✅ PASS [{elapsed:.2f}ms] : {test_file}")
                passed += 1
            except Exception as e:
                elapsed = (time.perf_counter() - start) * 1000
                print(f"  ❌ FAIL [{elapsed:.2f}ms] : {test_file}")
                print(f"     ↳ {e}")
                failed += 1

        print("\n-----------------------------------------------------")
        print(f"📊 Bilan des tests : {passed} réussis, {failed} échoués sur {total} au total.")
        print("-----------------------------------------------------")
        return failed == 0

if __name__ == "__main__":
    runner = AuraTestRunner()
    success = runner.run_all()
    sys.exit(0 if success else 1)
