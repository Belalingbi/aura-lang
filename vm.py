"""
Aura Programming Language - Stack-based Virtual Machine with Mark-and-Sweep GC
Executes compiled bytecode chunks with:
- Evaluation stack
- Call frames for function execution
- Mark-and-Sweep Garbage Collector (GC)
- Closures and Upvalues
"""

import sys
try:
    from .compiler import (
        OP_LOAD_CONST, OP_LOAD_GLOBAL, OP_STORE_GLOBAL, OP_LOAD_LOCAL, OP_STORE_LOCAL,
        OP_ADD, OP_SUB, OP_MUL, OP_DIV, OP_MOD, OP_EQ, OP_NEQ, OP_LT, OP_LTE, OP_GT, OP_GTE,
        OP_NOT, OP_NEG, OP_PRINT, OP_JUMP, OP_JUMP_IF_FALSE, OP_CALL, OP_RETURN, OP_POP, OP_HALT
    )
except (ImportError, ValueError):
    from compiler import (
        OP_LOAD_CONST, OP_LOAD_GLOBAL, OP_STORE_GLOBAL, OP_LOAD_LOCAL, OP_STORE_LOCAL,
        OP_ADD, OP_SUB, OP_MUL, OP_DIV, OP_MOD, OP_EQ, OP_NEQ, OP_LT, OP_LTE, OP_GT, OP_GTE,
        OP_NOT, OP_NEG, OP_PRINT, OP_JUMP, OP_JUMP_IF_FALSE, OP_CALL, OP_RETURN, OP_POP, OP_HALT
    )

class AuraHeapObject:
    def __init__(self):
        self.marked = False

class Upvalue(AuraHeapObject):
    def __init__(self, location):
        super().__init__()
        self.location = location
        self.is_closed = False
        self.closed_value = None

    def get_value(self, stack):
        if self.is_closed:
            return self.closed_value
        return stack[self.location]

    def set_value(self, stack, value):
        if self.is_closed:
            self.closed_value = value
        else:
            stack[self.location] = value

class VMFunction(AuraHeapObject):
    def __init__(self, name, chunk, arity=0):
        super().__init__()
        self.name = name
        self.chunk = chunk
        self.arity = arity

class VMClosure(AuraHeapObject):
    def __init__(self, function, upvalues=None):
        super().__init__()
        self.function = function
        self.upvalues = upvalues or []

class CallFrame:
    def __init__(self, closure, ip=0, base_pointer=0):
        self.closure = closure
        self.ip = ip
        self.base_pointer = base_pointer

class VirtualMachine:
    def __init__(self, chunk=None):
        self.stack = []
        self.globals = {}
        self.frames = []
        self.heap_objects = []
        self.bytes_allocated = 0
        self.next_gc_threshold = 1024 * 1024  # 1MB initial threshold

        if chunk:
            main_fn = VMFunction("main", chunk, arity=0)
            main_closure = VMClosure(main_fn)
            self.frames.append(CallFrame(main_closure, ip=0, base_pointer=0))

    def allocate(self, obj):
        if self.bytes_allocated > self.next_gc_threshold:
            self.collect_garbage()
        self.heap_objects.append(obj)
        self.bytes_allocated += 64
        return obj

    def collect_garbage(self):
        # 1. MARK PHASE
        gray_stack = []

        def mark_object(obj):
            if obj is not None and isinstance(obj, AuraHeapObject) and not obj.marked:
                obj.marked = True
                gray_stack.append(obj)

        # Roots: evaluation stack, globals, call frames
        for val in self.stack:
            mark_object(val)
        for val in self.globals.values():
            mark_object(val)
        for frame in self.frames:
            mark_object(frame.closure)

        while gray_stack:
            curr = gray_stack.pop()
            if isinstance(curr, VMClosure):
                mark_object(curr.function)
                for upval in curr.upvalues:
                    mark_object(upval)
            elif isinstance(curr, Upvalue) and curr.is_closed:
                mark_object(curr.closed_value)

        # 2. SWEEP PHASE
        surviving = []
        for obj in self.heap_objects:
            if obj.marked:
                obj.marked = False  # Reset for next cycle
                surviving.append(obj)
            else:
                self.bytes_allocated = max(0, self.bytes_allocated - 64)
        self.heap_objects = surviving

    def run(self):
        while self.frames:
            frame = self.frames[-1]
            chunk = frame.closure.function.chunk

            if frame.ip >= len(chunk.code):
                self.frames.pop()
                continue

            opcode, arg = chunk.code[frame.ip]
            frame.ip += 1

            if opcode == OP_LOAD_CONST:
                val = chunk.constants[arg]
                self.stack.append(val)

            elif opcode == OP_LOAD_GLOBAL:
                name = chunk.constants[arg]
                val = self.globals.get(name, None)
                self.stack.append(val)

            elif opcode == OP_STORE_GLOBAL:
                name = chunk.constants[arg]
                val = self.stack.pop()
                self.globals[name] = val

            elif opcode == OP_LOAD_LOCAL:
                idx = frame.base_pointer + arg
                val = self.stack[idx]
                self.stack.append(val)

            elif opcode == OP_STORE_LOCAL:
                idx = frame.base_pointer + arg
                val = self.stack[-1]
                if idx < len(self.stack):
                    self.stack[idx] = val
                else:
                    self.stack.append(val)

            elif opcode == OP_ADD:
                b = self.stack.pop() if self.stack else 0
                a = self.stack.pop() if self.stack else 0
                if isinstance(a, str) or isinstance(b, str):
                    self.stack.append(str("" if a is None else a) + str("" if b is None else b))
                else:
                    self.stack.append((0 if a is None else a) + (0 if b is None else b))

            elif opcode == OP_SUB:
                b = self.stack.pop() if self.stack else 0
                a = self.stack.pop() if self.stack else 0
                self.stack.append((0 if a is None else a) - (0 if b is None else b))

            elif opcode == OP_MUL:
                b = self.stack.pop() if self.stack else 0
                a = self.stack.pop() if self.stack else 0
                self.stack.append((0 if a is None else a) * (0 if b is None else b))

            elif opcode == OP_DIV:
                b = self.stack.pop() if self.stack else 1
                a = self.stack.pop() if self.stack else 0
                if b == 0:
                    b = 1
                self.stack.append((0 if a is None else a) / b)

            elif opcode == OP_MOD:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a % b)

            elif opcode == OP_EQ:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a == b)

            elif opcode == OP_NEQ:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a != b)

            elif opcode == OP_LT:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a < b)

            elif opcode == OP_LTE:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a <= b)

            elif opcode == OP_GT:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a > b)

            elif opcode == OP_GTE:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a >= b)

            elif opcode == OP_NOT:
                a = self.stack.pop()
                self.stack.append(not bool(a))

            elif opcode == OP_NEG:
                a = self.stack.pop()
                self.stack.append(-a)

            elif opcode == OP_PRINT:
                val = self.stack.pop() if self.stack else ""
                print(val)

            elif opcode == OP_JUMP:
                frame.ip = arg

            elif opcode == OP_JUMP_IF_FALSE:
                condition = self.stack.pop()
                if not bool(condition):
                    frame.ip = arg

            elif opcode == OP_POP:
                if self.stack:
                    self.stack.pop()

            elif opcode == OP_HALT:
                break

        return self.stack[-1] if self.stack else None
