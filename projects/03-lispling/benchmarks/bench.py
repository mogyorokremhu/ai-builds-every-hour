"""Time the tree-walking evaluator on a few programs: python benchmarks/bench.py"""
import sys, time, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from lispling import global_env, run

PROGRAMS = {
    "fib 20": "(define (fib n) (if (< n 2) n (+ (fib (- n 1)) (fib (- n 2))))) (fib 20)",
    "loop 200k": "(define (loop i a) (if (= i 0) a (loop (- i 1) (+ a i)))) (loop 200000 0)",
    "sum range 5k": "(reduce + 0 (map (lambda (x) (* x x)) (range 0 5000)))",
}


def bench(src, repeat=3):
    best = 1e9
    for _ in range(repeat):
        env = global_env()
        t = time.perf_counter()
        r = run(src, env)
        best = min(best, time.perf_counter() - t)
    return best, r


if __name__ == "__main__":
    print(f"{'program':<16}{'best (s)':>10}  result")
    for name, src in PROGRAMS.items():
        t, r = bench(src)
        print(f"{name:<16}{t:>10.3f}  {r}")
