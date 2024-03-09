import unittest
from PyENCRYPTO_utils.int_types import Uint64


class Uint64Test(unittest.TestCase):

    def test___add__(self):
        a = Uint64(2 ** 64 - 1)
        b = Uint64(1)

        self.assertTrue(isinstance(a.value, int))

        self.assertEqual(a + b, Uint64(0))
        self.assertTrue(isinstance(a + b, Uint64))
        self.assertEqual(a + 1, a.value + 1)
        self.assertTrue(isinstance(a + 1, int))

        self.assertEqual(a + Uint64(1), Uint64(0))
        self.assertTrue(isinstance(a + Uint64(1), Uint64))

    def test___sub__(self):
        a = Uint64(2 ** 64 - 1)
        b = Uint64(1)

        self.assertTrue(isinstance(a.value, int))

        self.assertEqual(a - b, Uint64(2 ** 64 - 2))
        self.assertTrue(isinstance(a - b, Uint64))
        self.assertEqual(a - 1, a.value - 1)
        self.assertTrue(isinstance(a - 1, int))

        self.assertEqual(a - Uint64(1), Uint64(2 ** 64 - 2))
        self.assertTrue(isinstance(a - Uint64(1), Uint64))

    def test___mul__(self):
        a = Uint64(2 ** 64 - 1)
        b = Uint64(2)

        self.assertTrue(isinstance(a.value, int))

        self.assertEqual(a * b, Uint64((2 ** 64 - 1) * 2))
        self.assertTrue(isinstance(a * b, Uint64))
        self.assertEqual(a * 2, a.value * 2)
        self.assertTrue(isinstance(a * 2, int))

        self.assertEqual(a * Uint64(2), Uint64((2 ** 64 - 1) * 2))
        self.assertTrue(isinstance(a * Uint64(2), Uint64))

        self.assertEqual(a * Uint64(-2), Uint64((2 ** 64 - 1) * -2))

    def test___str__(self):
        a = Uint64(2 ** 64 - 1)
        self.assertEqual(str(a), f"Uint64({2 ** 64 - 1})")
