"""
Aura Programming Language - Lexical Analyzer (Lexer)
Handles tokenization of Aura source code with support for:
- Literals (Numbers, Strings with escapes, F-Strings, Booleans, Nil)
- Keywords (Control flow, OOP, Functions, Concurrency, etc.)
- Multi-character operators and symbols (==, !=, <=, >=, ..., .., etc.)
- Comments (Single line // and multi-line /* ... */)
- Line and column tracking for clear error reporting
"""

class TokenType:
    KEYWORD = "KEYWORD"
    IDENTIFIER = "IDENTIFIER"
    NUMBER = "NUMBER"
    STRING = "STRING"
    FSTRING = "FSTRING"
    SYMBOL = "SYMBOL"
    EOF = "EOF"

class Token:
    def __init__(self, type_, value, line=1, column=1):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)}, L{self.line}:C{self.column})"

class LexerError(Exception):
    def __init__(self, message, line, column):
        super().__init__(f"LexerError at line {line}, col {column}: {message}")
        self.line = line
        self.column = column

class Lexer:
    KEYWORDS = {
        "fn", "class", "if", "else", "while", "for", "in", "return",
        "init", "__init__", "this", "self", "true", "false", "and", "or",
        "not", "import", "as", "try", "catch", "finally", "throw",
        "extends", "super", "static", "switch", "case", "default",
        "yield", "break", "continue", "nil", "None", "assert",
        "let", "mut", "go", "select", "set"
    }

    def __init__(self, code):
        self.code = code
        self.pos = 0
        self.line = 1
        self.column = 1
        self.current_char = self.code[self.pos] if self.code else None

    def advance(self):
        if self.current_char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1

        self.pos += 1
        if self.pos < len(self.code):
            self.current_char = self.code[self.pos]
        else:
            self.current_char = None

    def peek(self, offset=1):
        target_pos = self.pos + offset
        if target_pos < len(self.code):
            return self.code[target_pos]
        return None

    def skip_whitespace_and_comments(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.advance()
            elif self.current_char == '/' and self.peek() == '/':
                # Single-line comment
                while self.current_char is not None and self.current_char != '\n':
                    self.advance()
            elif self.current_char == '/' and self.peek() == '*':
                # Multi-line comment
                self.advance() # consume /
                self.advance() # consume *
                while self.current_char is not None:
                    if self.current_char == '*' and self.peek() == '/':
                        self.advance()
                        self.advance()
                        break
                    self.advance()
            else:
                break

    def number(self):
        start_col = self.column
        start_line = self.line
        result = ""
        has_dot = False
        while self.current_char is not None and (self.current_char.isdigit() or (self.current_char == '.' and not has_dot and self.peek() != '.')):
            if self.current_char == '.':
                # Don't treat range .. as float
                if self.peek() == '.':
                    break
                has_dot = True
            result += self.current_char
            self.advance()

        val = float(result) if has_dot else int(result)
        return Token(TokenType.NUMBER, val, start_line, start_col)

    def identifier_or_keyword(self):
        start_col = self.column
        start_line = self.line
        result = ""
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()

        token_type = TokenType.KEYWORD if result in self.KEYWORDS else TokenType.IDENTIFIER
        return Token(token_type, result, start_line, start_col)

    def string(self, quote_char='"'):
        start_col = self.column
        start_line = self.line
        self.advance() # Skip opening quote
        result = []
        while self.current_char is not None and self.current_char != quote_char:
            if self.current_char == '\\':
                self.advance()
                if self.current_char == 'n':
                    result.append('\n')
                elif self.current_char == 't':
                    result.append('\t')
                elif self.current_char == 'r':
                    result.append('\r')
                elif self.current_char == '\\':
                    result.append('\\')
                elif self.current_char == quote_char:
                    result.append(quote_char)
                else:
                    result.append(self.current_char)
            else:
                result.append(self.current_char)
            self.advance()

        if self.current_char != quote_char:
            raise LexerError(f"Unterminated string literal starting at line {start_line}, col {start_col}", start_line, start_col)

        self.advance() # Skip closing quote
        return Token(TokenType.STRING, "".join(result), start_line, start_col)

    def fstring(self):
        start_col = self.column
        start_line = self.line
        self.advance() # consume 'f'
        quote_char = self.current_char
        self.advance() # consume quote
        result = []
        while self.current_char is not None and self.current_char != quote_char:
            if self.current_char == '\\':
                self.advance()
                if self.current_char == quote_char:
                    result.append(quote_char)
                else:
                    result.append('\\' + (self.current_char if self.current_char else ''))
            else:
                result.append(self.current_char)
            self.advance()

        if self.current_char != quote_char:
            raise LexerError(f"Unterminated f-string literal at line {start_line}, col {start_col}", start_line, start_col)

        self.advance() # consume closing quote
        return Token(TokenType.FSTRING, "".join(result), start_line, start_col)

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace() or (self.current_char == '/' and (self.peek() in ('/', '*'))):
                self.skip_whitespace_and_comments()
                continue

            start_col = self.column
            start_line = self.line

            # Check for F-Strings (f"..." or f'...')
            if self.current_char == 'f' and self.peek() in ('"', "'"):
                return self.fstring()

            if self.current_char.isalpha() or self.current_char == '_':
                return self.identifier_or_keyword()

            if self.current_char.isdigit():
                return self.number()

            if self.current_char in ('"', "'"):
                return self.string(self.current_char)

            # Triple character symbols: ...
            if self.current_char == '.' and self.peek() == '.' and self.peek(2) == '.':
                self.advance()
                self.advance()
                self.advance()
                return Token(TokenType.SYMBOL, "...", start_line, start_col)

            # Double character symbols: ==, !=, <=, >=, +=, -=, *=, /=, &&, ||, ..
            if self.current_char == '=':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.SYMBOL, "==", start_line, start_col)
                return Token(TokenType.SYMBOL, "=", start_line, start_col)

            if self.current_char == '!':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.SYMBOL, "!=", start_line, start_col)
                return Token(TokenType.SYMBOL, "!", start_line, start_col)

            if self.current_char == '<':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.SYMBOL, "<=", start_line, start_col)
                return Token(TokenType.SYMBOL, "<", start_line, start_col)

            if self.current_char == '>':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.SYMBOL, ">=", start_line, start_col)
                return Token(TokenType.SYMBOL, ">", start_line, start_col)

            if self.current_char == '+':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.SYMBOL, "+=", start_line, start_col)
                return Token(TokenType.SYMBOL, "+", start_line, start_col)

            if self.current_char == '-':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.SYMBOL, "-=", start_line, start_col)
                return Token(TokenType.SYMBOL, "-", start_line, start_col)

            if self.current_char == '*':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.SYMBOL, "*=", start_line, start_col)
                return Token(TokenType.SYMBOL, "*", start_line, start_col)

            if self.current_char == '/':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.SYMBOL, "/=", start_line, start_col)
                return Token(TokenType.SYMBOL, "/", start_line, start_col)

            if self.current_char == '&' and self.peek() == '&':
                self.advance()
                self.advance()
                return Token(TokenType.SYMBOL, "&&", start_line, start_col)

            if self.current_char == '|' and self.peek() == '|':
                self.advance()
                self.advance()
                return Token(TokenType.SYMBOL, "||", start_line, start_col)

            if self.current_char == '.' and self.peek() == '.':
                self.advance()
                self.advance()
                return Token(TokenType.SYMBOL, "..", start_line, start_col)

            # Single character symbols
            if self.current_char in "+-*/%()[]{},.:;?@":
                char = self.current_char
                self.advance()
                return Token(TokenType.SYMBOL, char, start_line, start_col)

            raise LexerError(f"Unexpected character: {repr(self.current_char)}", start_line, start_col)

        return Token(TokenType.EOF, None, self.line, self.column)

    def tokenize(self):
        tokens = []
        while True:
            tok = self.get_next_token()
            tokens.append(tok)
            if tok.type == TokenType.EOF:
                break
        return tokens
