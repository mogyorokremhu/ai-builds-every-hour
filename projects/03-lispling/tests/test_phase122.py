"""Phase 122: rolling first/last/max/min to the seventh power."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase122(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield [float(x) for x in list(r(src))]

    # windows (1 2 3) (2 3 4) (3 4 5)
    def test_first_seventh(self):
        for v in self.each("(rolling-first-seventh '(1 2 3 4 5) 3)"):
            self.assertEqual(v, [1, 128, 2187])

    def test_last_seventh(self):
        for v in self.each("(rolling-last-seventh '(1 2 3 4 5) 3)"):
            self.assertEqual(v, [2187, 16384, 78125])

    def test_max_seventh(self):
        for v in self.each("(rolling-max-seventh '(1 2 3 4 5) 3)"):
            self.assertEqual(v, [2187, 16384, 78125])

    def test_min_seventh(self):
        for v in self.each("(rolling-min-seventh '(1 2 3 4 5) 3)"):
            self.assertEqual(v, [1, 128, 2187])


if __name__ == "__main__":
    unittest.main()
