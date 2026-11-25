"""Phase 117: rolling first/last/max/min to the fourth power."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase117(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield [float(x) for x in list(r(src))]

    # windows (3 6 9) (6 9 12) (9 12 3)
    def test_first_fourth(self):
        for v in self.each("(rolling-first-fourth '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [81, 1296, 6561])

    def test_last_fourth(self):
        for v in self.each("(rolling-last-fourth '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [6561, 20736, 81])

    def test_max_fourth(self):
        for v in self.each("(rolling-max-fourth '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [6561, 20736, 20736])

    def test_min_fourth(self):
        for v in self.each("(rolling-min-fourth '(3 6 9 12 3) 3)"):
            self.assertEqual(v, [81, 1296, 81])


if __name__ == "__main__":
    unittest.main()
