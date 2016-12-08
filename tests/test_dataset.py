import unittest
import benfordspy.dataset as dataset
import numpy as np


class TestDataset(unittest.TestCase):

    def test_datafirstdigits(self):
        d = dataset.dataset()
        d.datainit([1, 234, 5234, 6457, 345])
        d.updatefirstdigits()
        self.assertSequenceEqual(d.firstdigits.tolist(),
                                 np.array([1, 2, 5, 6, 3], dtype=int).tolist()
                                 )


if __name__ == '__main__':
    unittest.main()
