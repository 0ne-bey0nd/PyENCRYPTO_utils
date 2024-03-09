from PyENCRYPTO_utils.typedefs import *
import unittest


class TypedefsTest(unittest.TestCase):

    def test_test(self):
        self.assertEqual(REGISTER_SIZE, Uint64)

        self.assertEqual(REGISTER_SIZE.size(), 64)
        # self.assertEqual(LOG2_REGISTER_SIZE, ceil_log2(REGISTER_SIZE.size()))
