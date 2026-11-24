"""Phase 93: rolling first/last vs max, min vs first/last."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase93(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield [float(x) for x in list(r(src))]

    def test_first_minus_max(self):
        for v in self.each("(rolling-first-minus-max '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [-6, -6, -3])

    def test_last_minus_max(self):
        for v in self.each("(rolling-last-minus-max '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [0, 0, -9])

    def test_min_minus_first(self):
        for v in self.each("(rolling-min-minus-first '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [0, 0, -6])

    def test_min_minus_last(self):
        for v in self.each("(rolling-min-minus-last '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [-6, -6, 0])


if __name__ == "__main__":
    unittest.main()
