"""Time the tree-walker against the bytecode VM: python benchmarks/bench.py"""
import sys, time, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from lispling import global_env, run
from lispling.vm import run_vm

PROGRAMS = {
    "fib 20": "(define (fib n) (if (< n 2) n (+ (fib (- n 1)) (fib (- n 2))))) (fib 20)",
    "loop 200k": "(define (loop i a) (if (= i 0) a (loop (- i 1) (+ a i)))) (loop 200000 0)",
    "sum range 5k": "(reduce + 0 (map (lambda (x) (* x x)) (range 0 5000)))",
}


def bench(src, runner=run, repeat=3):
    best = 1e9
    for _ in range(repeat):
        env = global_env()
        t = time.perf_counter()
        r = runner(src, env)
        best = min(best, time.perf_counter() - t)
    return best, r


if __name__ == "__main__":
    print(f"{'program':<14}{'tree (s)':>10}{'vm (s)':>10}{'speedup':>9}  result")
    for name, src in PROGRAMS.items():
        t1, r1 = bench(src, run)
        t2, r2 = bench(src, run_vm)
        assert r1 == r2, (name, r1, r2)
        print(f"{name:<14}{t1:>10.3f}{t2:>10.3f}{t1 / t2:>8.2f}x  {r1}")
