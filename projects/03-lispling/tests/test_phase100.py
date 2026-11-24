"""Phase 100: rolling max+first, max+last, min+first, min+last."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase100(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield [float(x) for x in list(r(src))]

    def test_max_plus_first(self):
        for v in self.each("(rolling-max-plus-first '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [12, 18, 21])

    def test_max_plus_last(self):
        for v in self.each("(rolling-max-plus-last '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [18, 24, 15])

    def test_min_plus_first(self):
        for v in self.each("(rolling-min-plus-first '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [6, 12, 12])

    def test_min_plus_last(self):
        for v in self.each("(rolling-min-plus-last '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [12, 18, 6])


if __name__ == "__main__":
    unittest.main()
