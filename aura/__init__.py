"""
Aura Programming Language
A modern, dynamic, object-oriented language with AST interpreter, Bytecode VM, and CSP concurrency.
"""

__version__ = "1.0.0"

try:
    from .lexer import Lexer, TokenType, Token, LexerError
    from .parser import Parser, ParserError
    from .interpreter import Interpreter, Environment, AuraRuntimeError, AuraUserException
    from .compiler import Compiler
    from .vm import VirtualMachine
    from .concurrency import AuraChannel, AuraSupervisor, AuraConcurrencyManager
except (ImportError, ValueError):
    from lexer import Lexer, TokenType, Token, LexerError
    from parser import Parser, ParserError
    from interpreter import Interpreter, Environment, AuraRuntimeError, AuraUserException
    from compiler import Compiler
    from vm import VirtualMachine
    from concurrency import AuraChannel, AuraSupervisor, AuraConcurrencyManager

def run(code_or_file, env=None):
    interp = Interpreter()
    return interp.run(code_or_file, env=env)
