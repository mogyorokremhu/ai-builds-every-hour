"""Phase 121: rolling first/last/max/min to the sixth power."""
import unittest

from lispling.evaluator import run
from lispling.vm import run_vm

RUNNERS = (("tree", run), ("vm", run_vm))


class TestPhase121(unittest.TestCase):
    def each(self, src):
        for name, r in RUNNERS:
            with self.subTest(runner=name):
                yield [float(x) for x in list(r(src))]

    # windows (1 2 3) (2 3 4) (3 4 5)
    def test_first_sixth(self):
        for v in self.each("(rolling-first-sixth '(1 2 3 4 5) 3)"):
            self.assertEqual(v, [1, 64, 729])

    def test_last_sixth(self):
        for v in self.each("(rolling-last-sixth '(1 2 3 4 5) 3)"):
            self.assertEqual(v, [729, 4096, 15625])

    def test_max_sixth(self):
        for v in self.each("(rolling-max-sixth '(1 2 3 4 5) 3)"):
            self.assertEqual(v, [729, 4096, 15625])

    def test_min_sixth(self):
        for v in self.each("(rolling-min-sixth '(1 2 3 4 5) 3)"):
            self.assertEqual(v, [1, 64, 729])


if __name__ == "__main__":
    unittest.main()
