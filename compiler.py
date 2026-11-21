"""
Aura Programming Language - Bytecode Compiler
Translates Aura AST into bytecode chunks for the Stack-based Virtual Machine.
"""

try:
    from .parser import (
        AST, Program, VarAssign, FunctionDef, ReturnNode, IfNode, WhileNode,
        BinOp, UnaryOp, Num, StringNode, BoolNode, NilNode, Var, Call
    )
except (ImportError, ValueError):
    from parser import (
        AST, Program, VarAssign, FunctionDef, ReturnNode, IfNode, WhileNode,
        BinOp, UnaryOp, Num, StringNode, BoolNode, NilNode, Var, Call
    )

# Bytecode Opcodes
OP_LOAD_CONST = 1
OP_LOAD_GLOBAL = 2
OP_STORE_GLOBAL = 3
OP_LOAD_LOCAL = 4
OP_STORE_LOCAL = 5
OP_ADD = 6
OP_SUB = 7
OP_MUL = 8
OP_DIV = 9
OP_MOD = 10
OP_EQ = 11
OP_NEQ = 12
OP_LT = 13
OP_LTE = 14
OP_GT = 15
OP_GTE = 16
OP_NOT = 17
OP_NEG = 18
OP_PRINT = 19
OP_JUMP = 20
OP_JUMP_IF_FALSE = 21
OP_CALL = 22
OP_RETURN = 23
OP_POP = 24
OP_HALT = 25

class Chunk:
    def __init__(self, name="main"):
        self.name = name
        self.code = []       # List of (opcode, arg)
        self.constants = []  # Constant pool

    def emit(self, opcode, arg=None):
        self.code.append((opcode, arg))
        return len(self.code) - 1

    def add_constant(self, value):
        for idx, const in enumerate(self.constants):
            if const == value and type(const) == type(value):
                return idx
        self.constants.append(value)
        return len(self.constants) - 1

    def patch_jump(self, instruction_index, target_address):
        opcode, _ = self.code[instruction_index]
        self.code[instruction_index] = (opcode, target_address)

class Compiler:
    def __init__(self):
        self.current_chunk = Chunk()
        self.locals = []  # List of local variable names
        self.scope_depth = 0

    def compile(self, ast_node):
        self.visit(ast_node)
        self.current_chunk.emit(OP_HALT)
        return self.current_chunk

    def visit(self, node):
        method_name = f"visit_{type(node).__name__}"
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        pass

    def visit_Program(self, node):
        for stmt in node.statements:
            self.visit(stmt)

    def visit_Num(self, node):
        idx = self.current_chunk.add_constant(node.value)
        self.current_chunk.emit(OP_LOAD_CONST, idx)

    def visit_StringNode(self, node):
        idx = self.current_chunk.add_constant(node.value)
        self.current_chunk.emit(OP_LOAD_CONST, idx)

    def visit_BoolNode(self, node):
        idx = self.current_chunk.add_constant(node.value)
        self.current_chunk.emit(OP_LOAD_CONST, idx)

    def visit_NilNode(self, node):
        idx = self.current_chunk.add_constant(None)
        self.current_chunk.emit(OP_LOAD_CONST, idx)

    def visit_Var(self, node):
        # Check locals first
        for i in reversed(range(len(self.locals))):
            if self.locals[i] == node.name:
                self.current_chunk.emit(OP_LOAD_LOCAL, i)
                return
        idx = self.current_chunk.add_constant(node.name)
        self.current_chunk.emit(OP_LOAD_GLOBAL, idx)

    def visit_VarAssign(self, node):
        if node.value:
            self.visit(node.value)
        else:
            self.visit(NilNode())
        
        # Check if already local
        for i in reversed(range(len(self.locals))):
            if self.locals[i] == node.name:
                self.current_chunk.emit(OP_STORE_LOCAL, i)
                return
        if self.scope_depth > 0:
            self.locals.append(node.name)
            self.current_chunk.emit(OP_STORE_LOCAL, len(self.locals) - 1)
        else:
            idx = self.current_chunk.add_constant(node.name)
            self.current_chunk.emit(OP_STORE_GLOBAL, idx)

    def visit_FStringNode(self, node):
        import re
        parts = re.split(r'(\{.*?\})', node.template)
        first = True
        for part in parts:
            if not part:
                continue
            if part.startswith('{') and part.endswith('}'):
                expr_text = part[1:-1].strip()
                from lexer import Lexer
                from parser import Parser
                p = Parser(Lexer(expr_text))
                expr_ast = p.expression()
                self.visit(expr_ast)
            else:
                idx = self.current_chunk.add_constant(part)
                self.current_chunk.emit(OP_LOAD_CONST, idx)
            if not first:
                self.current_chunk.emit(OP_ADD)
            first = False
        if first:
            idx = self.current_chunk.add_constant("")
            self.current_chunk.emit(OP_LOAD_CONST, idx)

    def visit_TernaryNode(self, node):
        self.visit(node.condition)
        jump_false_idx = self.current_chunk.emit(OP_JUMP_IF_FALSE, 0)
        self.visit(node.true_expr)
        jump_end_idx = self.current_chunk.emit(OP_JUMP, 0)
        self.current_chunk.patch_jump(jump_false_idx, len(self.current_chunk.code))
        self.visit(node.false_expr)
        self.current_chunk.patch_jump(jump_end_idx, len(self.current_chunk.code))

    def visit_ReturnNode(self, node):
        if node.value:
            self.visit(node.value)
        else:
            idx = self.current_chunk.add_constant(None)
            self.current_chunk.emit(OP_LOAD_CONST, idx)
        self.current_chunk.emit(OP_RETURN)

    def visit_ClassDef(self, node):
        pass

    def visit_Get(self, node):
        self.visit(node.obj)

    def visit_Set(self, node):
        if node.value:
            self.visit(node.value)

    def visit_ListLiteral(self, node):
        idx = self.current_chunk.add_constant([el.value if hasattr(el, 'value') else str(el) for el in node.elements])
        self.current_chunk.emit(OP_LOAD_CONST, idx)

    def visit_BinOp(self, node):
        self.visit(node.left)
        self.visit(node.right)
        op_map = {
            "+": OP_ADD, "-": OP_SUB, "*": OP_MUL, "/": OP_DIV, "%": OP_MOD,
            "==": OP_EQ, "!=": OP_NEQ, "<": OP_LT, "<=": OP_LTE, ">": OP_GT, ">=": OP_GTE
        }
        opcode = op_map.get(node.op, OP_ADD)
        self.current_chunk.emit(opcode)

    def visit_UnaryOp(self, node):
        self.visit(node.expr)
        if node.op in ("not", "!"):
            self.current_chunk.emit(OP_NOT)
        elif node.op == "-":
            self.current_chunk.emit(OP_NEG)

    def visit_IfNode(self, node):
        self.visit(node.condition)
        jump_false_idx = self.current_chunk.emit(OP_JUMP_IF_FALSE, 0)
        
        for stmt in node.then_branch:
            self.visit(stmt)

        if node.else_branch:
            jump_end_idx = self.current_chunk.emit(OP_JUMP, 0)
            self.current_chunk.patch_jump(jump_false_idx, len(self.current_chunk.code))
            for stmt in node.else_branch:
                self.visit(stmt)
            self.current_chunk.patch_jump(jump_end_idx, len(self.current_chunk.code))
        else:
            self.current_chunk.patch_jump(jump_false_idx, len(self.current_chunk.code))

    def visit_WhileNode(self, node):
        loop_start = len(self.current_chunk.code)
        self.visit(node.condition)
        exit_jump = self.current_chunk.emit(OP_JUMP_IF_FALSE, 0)

        for stmt in node.body:
            self.visit(stmt)

        self.current_chunk.emit(OP_JUMP, loop_start)
        self.current_chunk.patch_jump(exit_jump, len(self.current_chunk.code))

    def visit_Call(self, node):
        # Special case for print()
        if isinstance(node.callee, Var) and node.callee.name == "print":
            for arg in node.arguments:
                self.visit(arg)
                self.current_chunk.emit(OP_PRINT)
            return

        for arg in node.arguments:
            self.visit(arg)
        self.visit(node.callee)
        self.current_chunk.emit(OP_CALL, len(node.arguments))
