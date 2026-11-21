"""
Aura Programming Language - Comprehensive Automated Verification Suite (test_suite.py)
Validates the complete Aura runtime, tools, and virtual machine.
"""

import sys
import os
import unittest
from lexer import Lexer, TokenType
from parser import Parser, Num, VarAssign, IfNode, ClassDef
from interpreter import Interpreter, AuraSet, AuraResponse
from compiler import Compiler
from vm import VirtualMachine
from concurrency import AuraChannel, AuraSupervisor

class TestAuraLexer(unittest.TestCase):
    def test_tokens(self):
        code = 'let x = 42.5; fn saluer(nom) { return f"Bonjour {nom}" }'
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        types = [t.type for t in tokens]
        self.assertIn(TokenType.KEYWORD, types)
        self.assertIn(TokenType.NUMBER, types)
        self.assertIn(TokenType.FSTRING, types)
        self.assertEqual(tokens[-1].type, TokenType.EOF)

class TestAuraParser(unittest.TestCase):
    def test_ast(self):
        code = "class Chien extends Animal { fn aboyer() { print(\"Wouf\") } }"
        lexer = Lexer(code)
        parser = Parser(lexer)
        ast = parser.parse()
        self.assertEqual(len(ast.statements), 1)
        self.assertIsInstance(ast.statements[0], ClassDef)
        self.assertEqual(ast.statements[0].name, "Chien")
        self.assertEqual(ast.statements[0].superclass, "Animal")

class TestAuraInterpreter(unittest.TestCase):
    def setUp(self):
        self.interp = Interpreter()

    def test_arithmetic_and_variables(self):
        code = """
        a = 10
        b = 25
        c = a + b * 2
        """
        self.interp.run(code)
        self.assertEqual(self.interp.global_env.get("c"), 60)

    def test_lambdas_and_map(self):
        code = """
        liste = [1, 2, 3]
        double = liste.map(fn(x) { return x * 2 })
        """
        self.interp.run(code)
        self.assertEqual(self.interp.global_env.get("double"), [2, 4, 6])

    def test_oop_and_inheritance(self):
        code = """
        class Parent {
            fn saluer() {
                return "Parent"
            }
        }
        class Enfant extends Parent {
            fn saluer() {
                return "Enfant"
            }
        }
        p = Parent()
        e = Enfant()
        res_p = p.saluer()
        res_e = e.saluer()
        """
        self.interp.run(code)
        self.assertEqual(self.interp.global_env.get("res_p"), "Parent")
        self.assertEqual(self.interp.global_env.get("res_e"), "Enfant")

class TestAuraConcurrency(unittest.TestCase):
    def test_channel(self):
        ch = AuraChannel(capacity=2)
        ch.send("msg1")
        ch.send("msg2")
        val1 = ch.receive()
        val2 = ch.receive()
        self.assertEqual(val1, "msg1")
        self.assertEqual(val2, "msg2")

class TestAuraVM(unittest.TestCase):
    def test_bytecode_execution(self):
        code = """
        x = 12
        y = 30
        res = x + y
        """
        parser = Parser(Lexer(code))
        ast = parser.parse()
        compiler = Compiler()
        chunk = compiler.compile(ast)
        vm = VirtualMachine(chunk)
        vm.run()
        self.assertEqual(vm.globals.get("res"), 42)

def run_tests():
    print("=====================================================")
    print("  TEST HARNESS OFFICIEL DU LANGAGE AURA 🌟")
    print("=====================================================")
    suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
