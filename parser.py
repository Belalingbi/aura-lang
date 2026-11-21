"""
Aura Programming Language - Parser & Abstract Syntax Tree (AST)
Translates token stream into AST with support for:
- Expressions (Arithmetic, Logical, Comparisons, Ternary, Calls, Ranges)
- Statements (Variable assignments, Destructuring, Loops, Conditionals, Switch)
- OOP (Classes, Inheritance, Constructors, Methods, Super, Static)
- Functions (Named, Anonymous/Lambdas, Variadic ...args, Decorators, Generators)
- Collections (Lists, Dicts, Sets, List Comprehensions)
- Error handling (Try / Catch / Finally / Throw)
- Concurrency (Go, Channels) & Modules (Import as)
"""

from lexer import TokenType, Token

# ==========================================
# AST NODES
# ==========================================

class AST:
    def __init__(self, line=1, column=1):
        self.line = line
        self.column = column

class Program(AST):
    def __init__(self, statements, line=1, column=1):
        super().__init__(line, column)
        self.statements = statements

class VarAssign(AST):
    def __init__(self, name, value, is_mut=True, line=1, column=1):
        super().__init__(line, column)
        self.name = name
        self.value = value
        self.is_mut = is_mut

class DestructuringAssignNode(AST):
    def __init__(self, targets, value, is_dict=False, line=1, column=1):
        super().__init__(line, column)
        self.targets = targets  # list of names or dict mapping
        self.value = value
        self.is_dict = is_dict

class FunctionDef(AST):
    def __init__(self, name, params, body, vararg=None, is_static=False, decorators=None, line=1, column=1):
        super().__init__(line, column)
        self.name = name
        self.params = params
        self.body = body
        self.vararg = vararg
        self.is_static = is_static
        self.decorators = decorators or []

class LambdaNode(AST):
    def __init__(self, params, body, vararg=None, line=1, column=1):
        super().__init__(line, column)
        self.params = params
        self.body = body
        self.vararg = vararg

class ReturnNode(AST):
    def __init__(self, value=None, line=1, column=1):
        super().__init__(line, column)
        self.value = value

class YieldNode(AST):
    def __init__(self, value=None, line=1, column=1):
        super().__init__(line, column)
        self.value = value

class BreakNode(AST):
    pass

class ContinueNode(AST):
    pass

class IfNode(AST):
    def __init__(self, condition, then_branch, else_branch=None, line=1, column=1):
        super().__init__(line, column)
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

class WhileNode(AST):
    def __init__(self, condition, body, line=1, column=1):
        super().__init__(line, column)
        self.condition = condition
        self.body = body

class ForNode(AST):
    def __init__(self, variable, iterable, body, line=1, column=1):
        super().__init__(line, column)
        self.variable = variable
        self.iterable = iterable
        self.body = body

class SwitchNode(AST):
    def __init__(self, expr, cases, default_body=None, line=1, column=1):
        super().__init__(line, column)
        self.expr = expr
        self.cases = cases  # list of (case_expr, body_statements)
        self.default_body = default_body

class ClassDef(AST):
    def __init__(self, name, superclass=None, methods=None, line=1, column=1):
        super().__init__(line, column)
        self.name = name
        self.superclass = superclass
        self.methods = methods or []

class TryNode(AST):
    def __init__(self, try_body, catch_var, catch_body, finally_body=None, line=1, column=1):
        super().__init__(line, column)
        self.try_body = try_body
        self.catch_var = catch_var
        self.catch_body = catch_body
        self.finally_body = finally_body

class ThrowNode(AST):
    def __init__(self, expr, line=1, column=1):
        super().__init__(line, column)
        self.expr = expr

class ImportNode(AST):
    def __init__(self, module_path, alias=None, line=1, column=1):
        super().__init__(line, column)
        self.module_path = module_path
        self.alias = alias

class GoNode(AST):
    def __init__(self, expr, line=1, column=1):
        super().__init__(line, column)
        self.expr = expr

class BinOp(AST):
    def __init__(self, left, op, right, line=1, column=1):
        super().__init__(line, column)
        self.left = left
        self.op = op
        self.right = right

class UnaryOp(AST):
    def __init__(self, op, expr, line=1, column=1):
        super().__init__(line, column)
        self.op = op
        self.expr = expr

class TernaryNode(AST):
    def __init__(self, condition, true_expr, false_expr, line=1, column=1):
        super().__init__(line, column)
        self.condition = condition
        self.true_expr = true_expr
        self.false_expr = false_expr

class RangeNode(AST):
    def __init__(self, start, end, line=1, column=1):
        super().__init__(line, column)
        self.start = start
        self.end = end

class Num(AST):
    def __init__(self, value, line=1, column=1):
        super().__init__(line, column)
        self.value = value

class StringNode(AST):
    def __init__(self, value, line=1, column=1):
        super().__init__(line, column)
        self.value = value

class FStringNode(AST):
    def __init__(self, template, line=1, column=1):
        super().__init__(line, column)
        self.template = template

class BoolNode(AST):
    def __init__(self, value, line=1, column=1):
        super().__init__(line, column)
        self.value = value

class NilNode(AST):
    def __init__(self, line=1, column=1):
        super().__init__(line, column)
        self.value = None

class Var(AST):
    def __init__(self, name, line=1, column=1):
        super().__init__(line, column)
        self.name = name

class Call(AST):
    def __init__(self, callee, arguments, varargs_spread=None, line=1, column=1):
        super().__init__(line, column)
        self.callee = callee
        self.arguments = arguments
        self.varargs_spread = varargs_spread

class Get(AST):
    def __init__(self, obj, member, line=1, column=1):
        super().__init__(line, column)
        self.obj = obj
        self.member = member

class Set(AST):
    def __init__(self, obj, member, value, line=1, column=1):
        super().__init__(line, column)
        self.obj = obj
        self.member = member
        self.value = value

class IndexGet(AST):
    def __init__(self, obj, index, line=1, column=1):
        super().__init__(line, column)
        self.obj = obj
        self.index = index

class IndexSet(AST):
    def __init__(self, obj, index, value, line=1, column=1):
        super().__init__(line, column)
        self.obj = obj
        self.index = index
        self.value = value

class ListLiteral(AST):
    def __init__(self, elements, line=1, column=1):
        super().__init__(line, column)
        self.elements = elements

class ListCompNode(AST):
    def __init__(self, expr, var_name, iterable, condition=None, line=1, column=1):
        super().__init__(line, column)
        self.expr = expr
        self.var_name = var_name
        self.iterable = iterable
        self.condition = condition

class DictLiteral(AST):
    def __init__(self, pairs, line=1, column=1):
        super().__init__(line, column)
        self.pairs = pairs  # list of (key_ast, val_ast)

class SuperNode(AST):
    def __init__(self, method=None, line=1, column=1):
        super().__init__(line, column)
        self.method = method


# ==========================================
# PARSER IMPLEMENTATION
# ==========================================

class ParserError(Exception):
    def __init__(self, message, line=1, column=1):
        super().__init__(f"ParserError at line {line}, col {column}: {message}")
        self.line = line
        self.column = column

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self, message):
        raise ParserError(message, self.current_token.line, self.current_token.column)

    def eat(self, token_type, value=None):
        if self.current_token.type == token_type:
            if value is None or self.current_token.value == value:
                tok = self.current_token
                self.current_token = self.lexer.get_next_token()
                return tok
            self.error(f"Expected value '{value}', but got '{self.current_token.value}'")
        self.error(f"Expected token type '{token_type}', but got '{self.current_token.type}' (value: '{self.current_token.value}')")

    def match(self, token_type, value=None):
        if self.current_token.type == token_type:
            if value is None or self.current_token.value == value:
                return True
        return False

    def skip_semicolons(self):
        while self.match(TokenType.SYMBOL, ";"):
            self.eat(TokenType.SYMBOL, ";")

    # ------------------------------------------
    # Entry Point
    # ------------------------------------------
    def parse(self):
        statements = []
        while not self.match(TokenType.EOF):
            self.skip_semicolons()
            if self.match(TokenType.EOF):
                break
            stmt = self.statement()
            if stmt:
                statements.append(stmt)
            self.skip_semicolons()
        return Program(statements)

    # ------------------------------------------
    # Statements
    # ------------------------------------------
    def statement(self):
        line = self.current_token.line
        col = self.current_token.column

        # Decorators (@decorator)
        decorators = []
        while self.match(TokenType.SYMBOL, "@"):
            self.eat(TokenType.SYMBOL, "@")
            deco_name = self.eat(TokenType.IDENTIFIER).value
            decorators.append(deco_name)

        if decorators:
            # Must be followed by a function definition
            if self.match(TokenType.KEYWORD, "fn"):
                return self.function_def(decorators=decorators)
            self.error("Decorators must precede a function definition")

        # Function definition (fn name(...) { ... })
        if self.match(TokenType.KEYWORD, "fn"):
            return self.function_def()

        # Class definition (class Name ...)
        if self.match(TokenType.KEYWORD, "class"):
            return self.class_def()

        # Variable declarations (let / mut)
        if self.match(TokenType.KEYWORD, "let") or self.match(TokenType.KEYWORD, "mut"):
            is_mut = self.current_token.value == "mut"
            self.eat(TokenType.KEYWORD)
            return self.variable_declaration(is_mut=is_mut)

        # Return statement
        if self.match(TokenType.KEYWORD, "return"):
            self.eat(TokenType.KEYWORD, "return")
            val = None
            if not self.match(TokenType.SYMBOL, ";") and not self.match(TokenType.SYMBOL, "}") and not self.match(TokenType.EOF):
                val = self.expression()
            return ReturnNode(val, line, col)

        # Yield statement
        if self.match(TokenType.KEYWORD, "yield"):
            self.eat(TokenType.KEYWORD, "yield")
            val = self.expression()
            return YieldNode(val, line, col)

        # Break
        if self.match(TokenType.KEYWORD, "break"):
            self.eat(TokenType.KEYWORD, "break")
            return BreakNode(line, col)

        # Continue
        if self.match(TokenType.KEYWORD, "continue"):
            self.eat(TokenType.KEYWORD, "continue")
            return ContinueNode(line, col)

        # If statement
        if self.match(TokenType.KEYWORD, "if"):
            return self.if_statement()

        # While loop
        if self.match(TokenType.KEYWORD, "while"):
            return self.while_statement()

        # For loop
        if self.match(TokenType.KEYWORD, "for"):
            return self.for_statement()

        # Switch / Case
        if self.match(TokenType.KEYWORD, "switch"):
            return self.switch_statement()

        # Try / Catch / Finally
        if self.match(TokenType.KEYWORD, "try"):
            return self.try_statement()

        # Throw
        if self.match(TokenType.KEYWORD, "throw"):
            self.eat(TokenType.KEYWORD, "throw")
            expr = self.expression()
            return ThrowNode(expr, line, col)

        # Import
        if self.match(TokenType.KEYWORD, "import"):
            return self.import_statement()

        # Go (goroutine / async task)
        if self.match(TokenType.KEYWORD, "go"):
            self.eat(TokenType.KEYWORD, "go")
            call_expr = self.expression()
            return GoNode(call_expr, line, col)

        # Assert statement (can also be parsed as expression/call)
        if self.match(TokenType.KEYWORD, "assert"):
            tok = self.eat(TokenType.KEYWORD, "assert")
            self.eat(TokenType.SYMBOL, "(")
            cond = self.expression()
            msg = None
            if self.match(TokenType.SYMBOL, ","):
                self.eat(TokenType.SYMBOL, ",")
                msg = self.expression()
            self.eat(TokenType.SYMBOL, ")")
            args = [cond]
            if msg:
                args.append(msg)
            return Call(Var("assert", tok.line, tok.column), args, line=line, column=col)

        # Destructuring Assignment: [a, b] = expr or {"a": x} = expr
        if self.match(TokenType.SYMBOL, "["):
            # Check if this is destructuring
            # We lookahead by parsing or checking assignment
            return self.destructuring_or_expr_statement()

        # Default: assignment or expression statement
        return self.expr_or_assign_statement()

    def variable_declaration(self, is_mut=True):
        line = self.current_token.line
        col = self.current_token.column
        name = self.eat(TokenType.IDENTIFIER).value
        val = None
        if self.match(TokenType.SYMBOL, "="):
            self.eat(TokenType.SYMBOL, "=")
            val = self.expression()
        return VarAssign(name, val, is_mut=is_mut, line=line, column=col)

    def destructuring_or_expr_statement(self):
        # Could be [a, b] = expr OR an array literal as expression
        line = self.current_token.line
        col = self.current_token.column
        self.eat(TokenType.SYMBOL, "[")
        
        elements = []
        is_destruct = True
        while not self.match(TokenType.SYMBOL, "]"):
            if self.match(TokenType.IDENTIFIER):
                elements.append(self.eat(TokenType.IDENTIFIER).value)
            else:
                is_destruct = False
                break
            if self.match(TokenType.SYMBOL, ","):
                self.eat(TokenType.SYMBOL, ",")
            else:
                break
        
        if is_destruct and self.match(TokenType.SYMBOL, "]"):
            self.eat(TokenType.SYMBOL, "]")
            if self.match(TokenType.SYMBOL, "="):
                self.eat(TokenType.SYMBOL, "=")
                val = self.expression()
                return DestructuringAssignNode(elements, val, is_dict=False, line=line, column=col)
        
        # If not destructuring, fallback: re-lex or construct list expr
        self.error("Malformed destructuring or expression statement")

    def expr_or_assign_statement(self):
        line = self.current_token.line
        col = self.current_token.column
        expr = self.expression()

        # Check for assignment operators: =, +=, -=, *=, /=
        if self.match(TokenType.SYMBOL, "="):
            self.eat(TokenType.SYMBOL, "=")
            val = self.expression()
            if isinstance(expr, Var):
                return VarAssign(expr.name, val, line=line, column=col)
            elif isinstance(expr, Get):
                return Set(expr.obj, expr.member, val, line=line, column=col)
            elif isinstance(expr, IndexGet):
                return IndexSet(expr.obj, expr.index, val, line=line, column=col)
            self.error("Invalid assignment target")

        for op_sym, bin_op in [("+=", "+"), ("-=", "-"), ("*=", "*"), ("/=", "/")]:
            if self.match(TokenType.SYMBOL, op_sym):
                self.eat(TokenType.SYMBOL, op_sym)
                right_val = self.expression()
                new_val = BinOp(expr, bin_op, right_val, line=line, column=col)
                if isinstance(expr, Var):
                    return VarAssign(expr.name, new_val, line=line, column=col)
                elif isinstance(expr, Get):
                    return Set(expr.obj, expr.member, new_val, line=line, column=col)
                elif isinstance(expr, IndexGet):
                    return IndexSet(expr.obj, expr.index, new_val, line=line, column=col)
                self.error("Invalid compound assignment target")

        return expr

    def block(self):
        self.eat(TokenType.SYMBOL, "{")
        statements = []
        while not self.match(TokenType.SYMBOL, "}") and not self.match(TokenType.EOF):
            self.skip_semicolons()
            if self.match(TokenType.SYMBOL, "}"):
                break
            stmt = self.statement()
            if stmt:
                statements.append(stmt)
            self.skip_semicolons()
        self.eat(TokenType.SYMBOL, "}")
        return statements

    def function_def(self, is_static=False, decorators=None):
        line = self.current_token.line
        col = self.current_token.column
        self.eat(TokenType.KEYWORD, "fn")
        
        # Method or function name (can be identifier or init/__init__)
        if self.match(TokenType.KEYWORD, "init") or self.match(TokenType.KEYWORD, "__init__"):
            name = self.eat(TokenType.KEYWORD).value
        else:
            name = self.eat(TokenType.IDENTIFIER).value

        self.eat(TokenType.SYMBOL, "(")
        params, vararg = self.parameter_list()
        self.eat(TokenType.SYMBOL, ")")

        body = self.block()
        return FunctionDef(name, params, body, vararg=vararg, is_static=is_static, decorators=decorators, line=line, column=col)

    def parameter_list(self):
        params = []
        vararg = None
        while not self.match(TokenType.SYMBOL, ")"):
            if self.match(TokenType.SYMBOL, "..."):
                self.eat(TokenType.SYMBOL, "...")
                vararg = self.eat(TokenType.IDENTIFIER).value
                break
            
            # Can be identifier or 'self' / 'this'
            if self.match(TokenType.KEYWORD, "self") or self.match(TokenType.KEYWORD, "this"):
                pname = self.eat(TokenType.KEYWORD).value
            else:
                pname = self.eat(TokenType.IDENTIFIER).value
            params.append(pname)

            if self.match(TokenType.SYMBOL, ","):
                self.eat(TokenType.SYMBOL, ",")
            else:
                break
        return params, vararg

    def class_def(self):
        line = self.current_token.line
        col = self.current_token.column
        self.eat(TokenType.KEYWORD, "class")
        name = self.eat(TokenType.IDENTIFIER).value

        superclass = None
        if self.match(TokenType.KEYWORD, "extends"):
            self.eat(TokenType.KEYWORD, "extends")
            superclass = self.eat(TokenType.IDENTIFIER).value

        self.eat(TokenType.SYMBOL, "{")
        methods = []
        while not self.match(TokenType.SYMBOL, "}") and not self.match(TokenType.EOF):
            self.skip_semicolons()
            if self.match(TokenType.SYMBOL, "}"):
                break
            
            is_static = False
            if self.match(TokenType.KEYWORD, "static"):
                self.eat(TokenType.KEYWORD, "static")
                is_static = True

            if self.match(TokenType.KEYWORD, "fn"):
                methods.append(self.function_def(is_static=is_static))
            elif self.match(TokenType.KEYWORD, "init") or self.match(TokenType.KEYWORD, "__init__"):
                # Constructor directly declared without 'fn'
                mname = self.eat(TokenType.KEYWORD).value
                self.eat(TokenType.SYMBOL, "(")
                params, vararg = self.parameter_list()
                self.eat(TokenType.SYMBOL, ")")
                body = self.block()
                methods.append(FunctionDef(mname, params, body, vararg=vararg, is_static=False, line=line, column=col))
            else:
                self.error(f"Unexpected token in class body: {self.current_token}")
            self.skip_semicolons()
        self.eat(TokenType.SYMBOL, "}")

        return ClassDef(name, superclass, methods, line=line, column=col)

    def if_statement(self):
        line = self.current_token.line
        col = self.current_token.column
        self.eat(TokenType.KEYWORD, "if")
        condition = self.expression()
        then_branch = self.block()
        else_branch = None

        if self.match(TokenType.KEYWORD, "else"):
            self.eat(TokenType.KEYWORD, "else")
            if self.match(TokenType.KEYWORD, "if"):
                else_branch = [self.if_statement()]
            else:
                else_branch = self.block()

        return IfNode(condition, then_branch, else_branch, line=line, column=col)

    def while_statement(self):
        line = self.current_token.line
        col = self.current_token.column
        self.eat(TokenType.KEYWORD, "while")
        condition = self.expression()
        body = self.block()
        return WhileNode(condition, body, line=line, column=col)

    def for_statement(self):
        line = self.current_token.line
        col = self.current_token.column
        self.eat(TokenType.KEYWORD, "for")

        has_paren = False
        if self.match(TokenType.SYMBOL, "("):
            self.eat(TokenType.SYMBOL, "(")
            has_paren = True

        var_name = self.eat(TokenType.IDENTIFIER).value
        self.eat(TokenType.KEYWORD, "in")
        iterable = self.expression()

        if has_paren:
            self.eat(TokenType.SYMBOL, ")")

        body = self.block()
        return ForNode(var_name, iterable, body, line=line, column=col)

    def switch_statement(self):
        line = self.current_token.line
        col = self.current_token.column
        self.eat(TokenType.KEYWORD, "switch")
        expr = self.expression()

        self.eat(TokenType.SYMBOL, "{")
        cases = []
        default_body = None

        while not self.match(TokenType.SYMBOL, "}") and not self.match(TokenType.EOF):
            self.skip_semicolons()
            if self.match(TokenType.KEYWORD, "case"):
                self.eat(TokenType.KEYWORD, "case")
                case_val = self.expression()
                self.eat(TokenType.SYMBOL, ":")
                case_stmts = []
                while not self.match(TokenType.KEYWORD, "case") and not self.match(TokenType.KEYWORD, "default") and not self.match(TokenType.SYMBOL, "}") and not self.match(TokenType.EOF):
                    self.skip_semicolons()
                    if self.match(TokenType.KEYWORD, "case") or self.match(TokenType.KEYWORD, "default") or self.match(TokenType.SYMBOL, "}"):
                        break
                    s = self.statement()
                    if s:
                        case_stmts.append(s)
                cases.append((case_val, case_stmts))
            elif self.match(TokenType.KEYWORD, "default"):
                self.eat(TokenType.KEYWORD, "default")
                self.eat(TokenType.SYMBOL, ":")
                default_stmts = []
                while not self.match(TokenType.KEYWORD, "case") and not self.match(TokenType.SYMBOL, "}") and not self.match(TokenType.EOF):
                    self.skip_semicolons()
                    if self.match(TokenType.KEYWORD, "case") or self.match(TokenType.SYMBOL, "}"):
                        break
                    s = self.statement()
                    if s:
                        default_stmts.append(s)
                default_body = default_stmts
            else:
                self.error(f"Expected 'case' or 'default', got {self.current_token}")
        self.eat(TokenType.SYMBOL, "}")

        return SwitchNode(expr, cases, default_body, line=line, column=col)

    def try_statement(self):
        line = self.current_token.line
        col = self.current_token.column
        self.eat(TokenType.KEYWORD, "try")
        try_body = self.block()

        catch_var = None
        catch_body = None
        if self.match(TokenType.KEYWORD, "catch"):
            self.eat(TokenType.KEYWORD, "catch")
            self.eat(TokenType.SYMBOL, "(")
            catch_var = self.eat(TokenType.IDENTIFIER).value
            self.eat(TokenType.SYMBOL, ")")
            catch_body = self.block()

        finally_body = None
        if self.match(TokenType.KEYWORD, "finally"):
            self.eat(TokenType.KEYWORD, "finally")
            finally_body = self.block()

        return TryNode(try_body, catch_var, catch_body, finally_body, line=line, column=col)

    def import_statement(self):
        line = self.current_token.line
        col = self.current_token.column
        self.eat(TokenType.KEYWORD, "import")
        path_token = self.eat(TokenType.STRING)
        module_path = path_token.value

        alias = None
        if self.match(TokenType.KEYWORD, "as"):
            self.eat(TokenType.KEYWORD, "as")
            alias = self.eat(TokenType.IDENTIFIER).value

        return ImportNode(module_path, alias, line=line, column=col)

    # ------------------------------------------
    # Expressions (Precedence Climbing)
    # ------------------------------------------
    def expression(self):
        return self.ternary()

    def ternary(self):
        line = self.current_token.line
        col = self.current_token.column
        expr = self.logical_or()

        if self.match(TokenType.SYMBOL, "?"):
            self.eat(TokenType.SYMBOL, "?")
            true_expr = self.expression()
            self.eat(TokenType.SYMBOL, ":")
            false_expr = self.expression()
            return TernaryNode(expr, true_expr, false_expr, line=line, column=col)

        return expr

    def logical_or(self):
        line = self.current_token.line
        col = self.current_token.column
        expr = self.logical_and()

        while self.match(TokenType.KEYWORD, "or") or self.match(TokenType.SYMBOL, "||"):
            op = self.current_token.value
            self.eat(self.current_token.type)
            right = self.logical_and()
            expr = BinOp(expr, op, right, line=line, column=col)

        return expr

    def logical_and(self):
        line = self.current_token.line
        col = self.current_token.column
        expr = self.equality()

        while self.match(TokenType.KEYWORD, "and") or self.match(TokenType.SYMBOL, "&&"):
            op = self.current_token.value
            self.eat(self.current_token.type)
            right = self.equality()
            expr = BinOp(expr, op, right, line=line, column=col)

        return expr

    def equality(self):
        line = self.current_token.line
        col = self.current_token.column
        expr = self.comparison()

        while self.match(TokenType.SYMBOL, "==") or self.match(TokenType.SYMBOL, "!="):
            op = self.current_token.value
            self.eat(TokenType.SYMBOL)
            right = self.comparison()
            expr = BinOp(expr, op, right, line=line, column=col)

        return expr

    def comparison(self):
        line = self.current_token.line
        col = self.current_token.column
        expr = self.range_expr()

        while self.current_token.type == TokenType.SYMBOL and self.current_token.value in ("<", "<=", ">", ">="):
            op = self.current_token.value
            self.eat(TokenType.SYMBOL)
            right = self.range_expr()
            expr = BinOp(expr, op, right, line=line, column=col)

        return expr

    def range_expr(self):
        line = self.current_token.line
        col = self.current_token.column
        expr = self.additive()

        if self.match(TokenType.SYMBOL, ".."):
            self.eat(TokenType.SYMBOL, "..")
            end_expr = self.additive()
            return RangeNode(expr, end_expr, line=line, column=col)

        return expr

    def additive(self):
        line = self.current_token.line
        col = self.current_token.column
        expr = self.multiplicative()

        while self.current_token.type == TokenType.SYMBOL and self.current_token.value in ("+", "-"):
            op = self.current_token.value
            self.eat(TokenType.SYMBOL)
            right = self.multiplicative()
            expr = BinOp(expr, op, right, line=line, column=col)

        return expr

    def multiplicative(self):
        line = self.current_token.line
        col = self.current_token.column
        expr = self.unary()

        while self.current_token.type == TokenType.SYMBOL and self.current_token.value in ("*", "/", "%"):
            op = self.current_token.value
            self.eat(TokenType.SYMBOL)
            right = self.unary()
            expr = BinOp(expr, op, right, line=line, column=col)

        return expr

    def unary(self):
        line = self.current_token.line
        col = self.current_token.column

        if self.match(TokenType.KEYWORD, "not") or self.match(TokenType.SYMBOL, "!"):
            op = self.current_token.value
            self.eat(self.current_token.type)
            return UnaryOp(op, self.unary(), line=line, column=col)

        if self.match(TokenType.SYMBOL, "-") or self.match(TokenType.SYMBOL, "+"):
            op = self.current_token.value
            self.eat(TokenType.SYMBOL)
            return UnaryOp(op, self.unary(), line=line, column=col)

        return self.call_and_access()

    def call_and_access(self):
        line = self.current_token.line
        col = self.current_token.column
        expr = self.primary()

        while True:
            # Function Call: expr(...)
            if self.match(TokenType.SYMBOL, "("):
                self.eat(TokenType.SYMBOL, "(")
                args = []
                varargs_spread = False
                while not self.match(TokenType.SYMBOL, ")"):
                    if self.match(TokenType.SYMBOL, "..."):
                        self.eat(TokenType.SYMBOL, "...")
                        vararg_expr = self.expression()
                        args.append(vararg_expr)
                        varargs_spread = True
                    else:
                        args.append(self.expression())
                    if self.match(TokenType.SYMBOL, ","):
                        self.eat(TokenType.SYMBOL, ",")
                    else:
                        break
                self.eat(TokenType.SYMBOL, ")")
                expr = Call(expr, args, varargs_spread=varargs_spread, line=line, column=col)

            # Member Access: expr.field
            elif self.match(TokenType.SYMBOL, "."):
                self.eat(TokenType.SYMBOL, ".")
                if self.match(TokenType.KEYWORD, "init") or self.match(TokenType.KEYWORD, "__init__"):
                    member = self.eat(TokenType.KEYWORD).value
                else:
                    member = self.eat(TokenType.IDENTIFIER).value
                expr = Get(expr, member, line=line, column=col)

            # Index Access: expr[idx]
            elif self.match(TokenType.SYMBOL, "["):
                self.eat(TokenType.SYMBOL, "[")
                idx = self.expression()
                self.eat(TokenType.SYMBOL, "]")
                expr = IndexGet(expr, idx, line=line, column=col)

            else:
                break

        return expr

    def primary(self):
        tok = self.current_token
        line = tok.line
        col = tok.column

        # Number
        if self.match(TokenType.NUMBER):
            self.eat(TokenType.NUMBER)
            return Num(tok.value, line, col)

        # String
        if self.match(TokenType.STRING):
            self.eat(TokenType.STRING)
            return StringNode(tok.value, line, col)

        # F-String
        if self.match(TokenType.FSTRING):
            self.eat(TokenType.FSTRING)
            return FStringNode(tok.value, line, col)

        # Boolean
        if self.match(TokenType.KEYWORD, "true"):
            self.eat(TokenType.KEYWORD, "true")
            return BoolNode(True, line, col)
        if self.match(TokenType.KEYWORD, "false"):
            self.eat(TokenType.KEYWORD, "false")
            return BoolNode(False, line, col)

        # Nil / None
        if self.match(TokenType.KEYWORD, "nil") or self.match(TokenType.KEYWORD, "None"):
            self.eat(TokenType.KEYWORD)
            return NilNode(line, col)

        # Super
        if self.match(TokenType.KEYWORD, "super"):
            self.eat(TokenType.KEYWORD, "super")
            method = None
            if self.match(TokenType.SYMBOL, "."):
                self.eat(TokenType.SYMBOL, ".")
                method = self.eat(TokenType.IDENTIFIER).value
            return SuperNode(method, line, col)

        # Anonymous Function / Lambda: fn(params) { body }
        if self.match(TokenType.KEYWORD, "fn"):
            self.eat(TokenType.KEYWORD, "fn")
            self.eat(TokenType.SYMBOL, "(")
            params, vararg = self.parameter_list()
            self.eat(TokenType.SYMBOL, ")")
            body = self.block()
            return LambdaNode(params, body, vararg=vararg, line=line, column=col)

        # Identifiers & Keywords used as variables (this, self, set, etc.)
        if self.match(TokenType.IDENTIFIER):
            self.eat(TokenType.IDENTIFIER)
            return Var(tok.value, line, col)
        if self.match(TokenType.KEYWORD, "this") or self.match(TokenType.KEYWORD, "self"):
            self.eat(TokenType.KEYWORD)
            return Var(tok.value, line, col)
        if self.match(TokenType.KEYWORD, "set"):
            self.eat(TokenType.KEYWORD, "set")
            return Var("set", line, col)

        # Grouping: ( expr )
        if self.match(TokenType.SYMBOL, "("):
            self.eat(TokenType.SYMBOL, "(")
            expr = self.expression()
            self.eat(TokenType.SYMBOL, ")")
            return expr

        # List Literal or List Comprehension: [ a, b ] or [ expr for x in iter if cond ]
        if self.match(TokenType.SYMBOL, "["):
            self.eat(TokenType.SYMBOL, "[")
            if self.match(TokenType.SYMBOL, "]"):
                self.eat(TokenType.SYMBOL, "]")
                return ListLiteral([], line, col)

            first = self.expression()
            # Check for List Comprehension: [ first for x in iter ... ]
            if self.match(TokenType.KEYWORD, "for"):
                self.eat(TokenType.KEYWORD, "for")
                var_name = self.eat(TokenType.IDENTIFIER).value
                self.eat(TokenType.KEYWORD, "in")
                iterable = self.expression()
                condition = None
                if self.match(TokenType.KEYWORD, "if"):
                    self.eat(TokenType.KEYWORD, "if")
                    condition = self.expression()
                self.eat(TokenType.SYMBOL, "]")
                return ListCompNode(first, var_name, iterable, condition, line, col)

            # Normal List Literal
            elements = [first]
            while self.match(TokenType.SYMBOL, ","):
                self.eat(TokenType.SYMBOL, ",")
                if self.match(TokenType.SYMBOL, "]"):
                    break
                elements.append(self.expression())
            self.eat(TokenType.SYMBOL, "]")
            return ListLiteral(elements, line, col)

        # Dict Literal: { key: value, ... }
        if self.match(TokenType.SYMBOL, "{"):
            self.eat(TokenType.SYMBOL, "{")
            pairs = []
            while not self.match(TokenType.SYMBOL, "}") and not self.match(TokenType.EOF):
                key = self.expression()
                self.eat(TokenType.SYMBOL, ":")
                val = self.expression()
                pairs.append((key, val))
                if self.match(TokenType.SYMBOL, ","):
                    self.eat(TokenType.SYMBOL, ",")
                else:
                    break
            self.eat(TokenType.SYMBOL, "}")
            return DictLiteral(pairs, line, col)

        self.error(f"Unexpected token in primary expression: {tok}")
