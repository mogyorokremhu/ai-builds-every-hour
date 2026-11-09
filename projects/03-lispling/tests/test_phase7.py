import unittest
from lispling import run, global_env
from lispling.types import to_string
from lispling.pairs import Pair
from lispling.diagnostics import parse_checked, SourceError


def ev(src):
    return run(src, global_env())


class Dotted(unittest.TestCase):
    def test_cons_atom(self):
        r = ev("(cons 1 2)")
        self.assertIsInstance(r, Pair)
        self.assertEqual(to_string(r), "(1 . 2)")

    def test_car_cdr(self):
        self.assertEqual(ev("(car (cons 1 2))"), 1)
        self.assertEqual(ev("(cdr (cons 1 2))"), 2)

    def test_read_dotted(self):
        self.assertEqual(to_string(ev("'(1 2 . 3)")), "(1 2 . 3)")

    def test_dot_list_tail_collapses(self):
        self.assertEqual(ev("'(1 . (2 3))"), [1, 2, 3])

    def test_cons_onto_pair(self):
        self.assertEqual(to_string(ev("(cons 0 (cons 1 2))")), "(0 1 . 2)")

    def test_pair_pred(self):
        self.assertIs(ev("(pair? (cons 1 2))"), True)
        self.assertIs(ev("(pair? '(1))"), True)
        self.assertIs(ev("(pair? '())"), False)

    def test_equal(self):
        self.assertIs(ev("(equal? (cons 1 2) (cons 1 2))"), True)

    def test_list_pred_false_for_dotted(self):
        self.assertIs(ev("(list? (cons 1 2))"), False)

    def test_checked_reader(self):
        self.assertEqual(to_string(parse_checked("'(a . b)")[0][1]), "(a . b)")
        with self.assertRaises(SourceError):
            parse_checked("(a . b c)")


if __name__ == "__main__":
    unittest.main()
