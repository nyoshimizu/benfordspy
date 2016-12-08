import unittest
from benfordspy.numerics import *


class TestNumerics(unittest.TestCase):

    def test_digitn(self):
        self.assertEqual(digitn(1, 34823), 3)
        self.assertEqual(digitn(2, 34823), 4)
        self.assertEqual(digitn(3, 34823), 8)
        self.assertEqual(digitn(4, 34823), 2)
        self.assertEqual(digitn(5, 34823), 3)
        self.assertEqual(digitn(6, 34823), 0)

        self.assertEqual(digitn(1, 0.23), 2)
        self.assertEqual(digitn(2, 0.23), 3)

    def test_magnitudein(self):
        array = np.array([1, 123, 234, 12345])
        self.assertEqual(magnitudebin(array), {0: 1, 1: 0, 2: 2, 3: 0, 4: 1})

    def test_benfords(self):
        benfordslaw = [.301, .176, .125, .097, .079, .067, .058, .051, .046]

        for k in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            self.assertAlmostEqual(benfords(k), benfordslaw[k-1], places=3)

    def test_ktest(self):

        testfirstdigits = np.array([1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4,
                                    4, 4, 4, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 8,
                                    8, 9])
        self.assertAlmostEqual(kuipertest(testfirstdigits, plot=False),
                               0.21, places=2)

if __name__ == '__main__':
    unittest.main(exit=False)
