"""
This class contains the dataset.
"""

import numpy as np
import numerics
import unittest


class dataset:

    def __init__(self):
        self.data = np.empty([1], dtype=float)
        self.firstdigits = np.empty([1], dtype=int)

    def datainit(self, loadlist):
        """
        Initialize to data array.

        :param loadlist: 1-D list to be initialized into dataset.

        :return: Return 0 for failure, 1 for successful append.
        """

        if type(loadlist) is not list:
            print("Input is not a list, but of type {}.\n".
                  format(type(loadlist)))
            return 0

        nplist = np.array(loadlist, dtype=float)

        if nplist.ndim != 1:
            print("Input is not 1-D.\n")
            return 0

        self.data = np.array(nplist, dtype=float)

    def dataarrayappend(self, appendlist):
        """
        Append a list of values to existing data array, then sorted.

        :param appendlist: A single-row Python list of number values to be added
        to the dataset.

        :return: Return 0 for failure, 1 for successful append.
        """

        if type(appendlist) is not list:
            print("Input is not a list, but of type {}.\n".
                  format(type(appendlist)))
            return 0

        nplist = np.array(appendlist, dtype=float)

        if nplist.ndim != 1:
            print("Input is not 1-D.\n")
            return 0

        self.data = np.concatenate(self.data, nplist)

        self.data = np.sort(self.data)

    def updatefirstdigits(self):
        """
        Update list of first digits of self.data.

        :return: Return 0 for failure, 1 for successful update.
        """

        firstdigit = np.vectorize(numerics.digitn)

        self.firstdigits = firstdigit(1, self.data)

        self.firstdigits = self.firstdigits.astype(int)

        # Superficial return
        return 1


class TestNumerics(unittest.TestCase):

    def test_datafirstdigits(self):
        d = dataset()
        d.datainit([1, 234, 5234, 6457, 345])
        d.updatefirstdigits()
        self.assertSequenceEqual(d.firstdigits.tolist(),
                                 np.array([1, 2, 5, 6, 3], dtype=int).tolist()
                                 )


if __name__ == '__main__':
    unittest.main()
