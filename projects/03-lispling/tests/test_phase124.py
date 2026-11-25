"""Phase 124: rolling first/last/max/min to the eighth power."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase124(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield [float(x) for x in list(r(src))]

    def test_first_eighth(self):
        for v in self.each("(rolling-first-eighth '(1 2 3 4 5) 3)"):
            self.assertEqual(v, [1, 2**8, 3**8])

    def test_last_eighth(self):
        for v in self.each("(rolling-last-eighth '(1 2 3 4 5) 3)"):
            self.assertEqual(v, [3**8, 4**8, 5**8])

    def test_max_eighth(self):
        for v in self.each("(rolling-max-eighth '(1 2 3 4 5) 3)"):
            self.assertEqual(v, [3**8, 4**8, 5**8])

    def test_min_eighth(self):
        for v in self.each("(rolling-min-eighth '(1 2 3 4 5) 3)"):
            self.assertEqual(v, [1, 2**8, 3**8])


if __name__ == "__main__":
    unittest.main()
