"""Bytecode compiler + stack VM for a core subset of Lispling.

Supported forms: constants, symbols, quote, if, define, set!, lambda, begin,
let (incl. named let), let*, letrec, do, quasiquote, cond (with else), and, or,
and procedure calls. Constant arithmetic on literals is folded at compile time.
Calls in tail position reuse the current frame, so loops run in constant Python stack.
Macros (define-macro) are expanded at compile time against the compile env.
"""
from __future__ import annotations
from .evaluator import global_env, _lookup_macro, expand_macro
from .forms import EXPANDERS
from .reader import parse
from .types import Env, Lambda, LispError, Macro, Symbol, to_string

_CENV: Env | None = None  # env macros are looked up in while compiling

(CONST, LOAD, STORE, DEF, JUMP, JF, JF_KEEP, JT_KEEP, POP, CALL, TAILCALL,
 RET, MAKE) = range(13)
NAMES = ["CONST", "LOAD", "STORE", "DEF", "JUMP", "JF", "JF_KEEP", "JT_KEEP",
         "POP", "CALL", "TAILCALL", "RET", "MAKE"]


class Code:
    def __init__(self, params=(), name=""):
        self.ops: list[tuple[int, object]] = []
        self.params, self.name = list(params), name

    def emit(self, op, arg=None):
        self.ops.append((op, arg))
        return len(self.ops) - 1

    def patch(self, at):
        self.ops[at] = (self.ops[at][0], len(self.ops))


class VMClosure:
    def __init__(self, code: Code, env: Env):
        self.code, self.env, self.name = code, env, code.name

    def __call__(self, *args):
        return execute(self, list(args))


def compile_expr(x, code: Code, tail: bool):
    if isinstance(x, Symbol):
        code.emit(LOAD, x)
    elif not isinstance(x, list):
        code.emit(CONST, x)
    elif not x:
        raise LispError("cannot evaluate empty list ()")
    else:
        head = x[0]
        form = _FORMS.get(head) if isinstance(head, Symbol) else None
        if form is None and isinstance(head, Symbol) and _CENV is not None:
            m = _lookup_macro(head, _CENV)
            if m is not None:
                return compile_expr(expand_macro(m, x[1:]), code, tail)
        if form is None and isinstance(head, Symbol):
            x = [x[0]] + [_pre(a) for a in x[1:]]
            v = _fold(x)
            if v is not None:
                code.emit(CONST, v)
                return _end(code, tail)
        if form:
            form(x, code, tail)
            return
        compile_expr(head, code, False)
        for a in x[1:]:
            compile_expr(a, code, False)
        code.emit(TAILCALL if tail else CALL, len(x) - 1)
        return
    if tail:
        code.emit(RET)


def _pre(a):
    """Fold nested constant arithmetic inside an operand."""
    if isinstance(a, list) and a and isinstance(a[0], Symbol) and a[0] in _FOLD:
        a = [a[0]] + [_pre(b) for b in a[1:]]
        v = _fold(a)
        return a if v is None else v
    return a


def _end(code, tail):
    if tail:
        code.emit(RET)


def _body(forms, code, tail):
    if not forms:
        code.emit(CONST, [])
        return _end(code, tail)
    for i, f in enumerate(forms):
        last = i == len(forms) - 1
        compile_expr(f, code, tail and last)
        if not last:
            code.emit(POP)


def _quote(x, code, tail):
    code.emit(CONST, x[1])
    _end(code, tail)


def _if(x, code, tail):
    if len(x) < 3:
        raise LispError("if needs a test and a branch")
    compile_expr(x[1], code, False)
    jf = code.emit(JF)
    compile_expr(x[2], code, tail)
    j = None if tail else code.emit(JUMP)
    code.patch(jf)
    if len(x) > 3:
        compile_expr(x[3], code, tail)
    else:
        code.emit(CONST, [])
        _end(code, tail)
    if j is not None:
        code.patch(j)


def _define(x, code, tail):
    target = x[1]
    if isinstance(target, list):
        code.emit(MAKE, _lambda_code(target[1:], x[2:], target[0]))
        name = target[0]
    else:
        compile_expr(x[2], code, False)
        name = target
    code.emit(DEF, name)
    _end(code, tail)


def _define_macro(x, code, tail):
    if len(x) < 3 or not isinstance(x[1], list) or not x[1]:
        raise LispError("define-macro needs (name params...) and a body")
    if _CENV is None:
        raise LispError("define-macro needs a compile environment")
    _CENV[x[1][0]] = Macro(x[1][1:], x[2:], _CENV, x[1][0])
    code.emit(CONST, [])
    _end(code, tail)


def _set(x, code, tail):
    compile_expr(x[2], code, False)
    code.emit(STORE, x[1])
    _end(code, tail)


def _lambda_code(params, body, name=""):
    c = Code(params, name)
    _body(body, c, True)
    return c


def _lambda(x, code, tail):
    code.emit(MAKE, _lambda_code(x[1], x[2:]))
    _end(code, tail)


def _begin(x, code, tail):
    _body(x[1:], code, tail)


def _let_ok(x, code, tail):
    if not isinstance(x[1], list):
        # (let loop ((v init)...) body) => ((lambda () (define loop (lambda (v...) body)) (loop init...)))
        loop, binds = x[1], x[2]
        lam = [Symbol("lambda"), [b[0] for b in binds], *x[3:]]
        call = [Symbol("define"), loop, lam]
        return compile_expr([[Symbol("lambda"), [], call, [loop, *[b[1] for b in binds]]]], code, tail)
    names = [b[0] for b in x[1]]
    code.emit(MAKE, _lambda_code(names, x[2:]))
    for b in x[1]:
        compile_expr(b[1], code, False)
    code.emit(TAILCALL if tail else CALL, len(names))


def _expander(fn):
    def f(x, code, tail):
        compile_expr(fn(x), code, tail)
    return f


_FOLD = {"+": lambda *a: sum(a), "-": lambda a, *r: -a if not r else a - sum(r),
         "*": lambda *a: __import__("math").prod(a)}


def _fold(x):
    """Fold (+ 1 2) style calls whose operands are all int literals; else None."""
    h = x[0]
    if isinstance(h, Symbol) and h in _FOLD and len(x) > 1 and all(
            type(a) is int for a in x[1:]):
        return _FOLD[h](*x[1:])
    return None


def _cond(x, code, tail):
    ends = []
    for clause in x[1:]:
        test, body = clause[0], clause[1:]
        if test == "else":
            _body(body, code, tail)
            break
        compile_expr(test, code, False)
        jf = code.emit(JF)
        _body(body, code, tail)
        if not tail:
            ends.append(code.emit(JUMP))
        code.patch(jf)
    else:
        code.emit(CONST, [])
        _end(code, tail)
    for e in ends:
        code.patch(e)


def _logic(op, empty):
    def f(x, code, tail):
        if len(x) == 1:
            code.emit(CONST, empty)
            return _end(code, tail)
        jumps = []
        for a in x[1:-1]:
            compile_expr(a, code, False)
            jumps.append(code.emit(op))
        compile_expr(x[-1], code, tail)
        for j in jumps:
            code.patch(j)
        if tail and jumps:
            code.emit(RET)
    return f


_FORMS = {"quote": _quote, "if": _if, "define": _define, "set!": _set, "define-macro": _define_macro,
          "lambda": _lambda, "begin": _begin, "let": _let_ok, "cond": _cond,
          **{k: _expander(v) for k, v in EXPANDERS.items()},
          "and": _logic(JF_KEEP, True), "or": _logic(JT_KEEP, False)}


def compile_toplevel(x, env: Env | None = None) -> Code:
    """Compile one top-level form; env (if given) is where macros are found/defined."""
    global _CENV
    old, _CENV = _CENV, env
    try:
        c = Code()
        compile_expr(x, c, True)
        return c
    finally:
        _CENV = old


def disassemble(code: Code, indent="") -> str:
    out = []
    for i, (op, arg) in enumerate(code.ops):
        if isinstance(arg, Code):
            out.append(f"{indent}{i:3} {NAMES[op]} <code {arg.name or 'lambda'}>")
            out.append(disassemble(arg, indent + "      "))
        else:
            out.append(f"{indent}{i:3} {NAMES[op]:<9}{'' if arg is None else to_string(arg)}")
    return "\n".join(out)


def execute(closure: VMClosure, args: list, toplevel=False):
    """Run a closure to completion with an explicit frame stack."""
    base = []  # saved frames: (code, pc, env, stack)
    code, env = closure.code, (closure.env if toplevel else Env(closure.env))
    if not toplevel:
        _bind(closure, env, args)
    pc, stack = 0, []
    while True:
        op, arg = code.ops[pc]
        pc += 1
        if op == CONST:
            stack.append(arg)
        elif op == LOAD:
            stack.append(env.find(arg)[arg])
        elif op == STORE:
            env.find(arg)[arg] = stack.pop()
            stack.append([])
        elif op == DEF:
            v = stack.pop()
            if isinstance(v, VMClosure) and not v.name:
                v.name = arg
            env[arg] = v
            stack.append(arg)
        elif op == JUMP:
            pc = arg
        elif op == JF:
            if stack.pop() is False:
                pc = arg
        elif op == JF_KEEP:
            if stack[-1] is False:
                pc = arg
            else:
                stack.pop()
        elif op == JT_KEEP:
            if stack[-1] is not False:
                pc = arg
            else:
                stack.pop()
        elif op == POP:
            stack.pop()
        elif op == MAKE:
            stack.append(VMClosure(arg, env))
        elif op == RET:
            v = stack.pop()
            if not base:
                return v
            code, pc, env, stack = base.pop()
            stack.append(v)
        elif op in (CALL, TAILCALL):
            n = arg
            cargs = stack[len(stack) - n:] if n else []
            del stack[len(stack) - n:]
            f = stack.pop()
            if isinstance(f, VMClosure):
                if op == CALL:
                    base.append((code, pc, env, stack))
                    stack = []
                else:
                    stack = []
                code, pc = f.code, 0
                env = Env(f.env)
                _bind(f, env, cargs)
            elif isinstance(f, Lambda) or callable(f):
                try:
                    v = f(*cargs) if not isinstance(f, Lambda) else _tree(f, cargs)
                except TypeError as e:
                    raise LispError(f"bad call: {e}") from None
                if op == CALL:
                    stack.append(v)
                else:
                    if not base:
                        return v
                    code, pc, env, stack = base.pop()
                    stack.append(v)
            else:
                raise LispError(f"not a procedure: {to_string(f)}")


def _bind(f, env, args):
    if len(args) != len(f.code.params):
        raise LispError(f"{f.name or 'lambda'} expects {len(f.code.params)} args, got {len(args)}")
    env.update(zip(f.code.params, args))


def _tree(f: Lambda, args):
    from .evaluator import evaluate
    env = Env(f.env)
    env.update(zip(f.params, args))
    r = []
    for e in f.body:
        r = evaluate(e, env)
    return r


def run_vm(src: str, env: Env | None = None):
    """Compile and run every top-level expression of src on the VM."""
    env = env if env is not None else global_env()
    result = []
    for e in parse(src):
        result = execute(VMClosure(compile_toplevel(e, env), env), [], toplevel=True)
    return result
