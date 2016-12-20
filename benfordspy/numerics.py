"""
This contains functions to perform some important numerical work.
"""

import numpy as np
import matplotlib.pyplot as mptlib


class benfords:

    """
    Define PDF and CDF for Benford's law.
    """

    def __init__(self):
        self.pdf = self.benfpdf()
        self.cdf = self.benfcdf()

    def benfords(self, firstdigit):
        """
        Calculates, based on Benford's law, the probability that the leading digit
        is equal to firstdigit (1-9) in base 10.

        :param firstdigit: Numerical value of first digit of a number.

        :return: Benford's law probability of firstidigit as first digit of a
        number.
        """

        return np.log10(1 + 1 / firstdigit)

    def benfpdf(self):
        """
        Calculate Benford's law probability distribution function for first
        significant digits. Return a dictionary, where key is digit and value
        is probability.

        :return: dict of Benford's Law PDF for first significant digits.
        """

        benfpdf = {}

        for k in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            benfpdf[k] = self.benfords(k)

        assert sum(benfpdf.values()) == 1

        return benfpdf

    def benfcdf(self):
        """
        Calculate Benford's law cumulative distribution function for first
        significant digits. Return a dictionary, where key is digit and value
        is probability.

        :return: dict of Benford's Law CDF for first significant digits.
        """

        benfpdf = self.benfpdf()

        benfcdf = {}

        for k in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            benfcdf[k] = sum([benfpdf[m] for m in benfpdf.keys()
                              if m <= k])

        assert benfcdf[9] == 1

        return benfcdf


def digitn(n, number):
    """
    Returns nth digit, where 1 is the most significant digit, of input number.
    E.g., inputs of n=4, number=38,492 returns 9.

    :param n: Significant digit to return.
    :param number: Number to be examined.

    :return: The nth significant digit of number.
    """

    if number == 0:
        return 0

    nlog10 = np.log10(n)

    mostsigplace = np.floor(np.log10(np.absolute(number)))

    sigplacen = mostsigplace-(n-1)

    n = np.floor(number/10**sigplacen)
    temp = 10*np.floor(n/10)
    n -= temp

    return n


def test(testtype, firstdigits, plot=False, printsignificance=False):
    """
    Combine all tests into one function. Calculates Benford's law PDF and CDF,
    then calculates the test value (e.g. Kuiper's, etc.). Then outputs plot
    or prints significance results, and returns test value.

    :param testtype: String of type of test to perform: Kuiper, KS, m, or d.
    :param firstdigits: Numpy array of first digits, usually passed in using
    dataset.dataset class.
    :param plot: Boolean of whether to plot PDF result.
    :param printsignificance: Boolean of whether to print significance test
    results to output.

    :return: Returns test value.
    """

    testvar = {"Kuiper": "V",
               "KS": "D",
               "m": "m",
               "d": "d"
               }

    testname = {"Kuiper": "Kuiper's",
                "KS": "Kolmogorov-Smirnov",
                "m": "Leemis\'",
                "d": "Cho-Gaines\'"
                }

    # Calculate Benford's law PDF ##############################################
    benfpdf = benfords().pdf
    npbenfpdf = np.array([benfpdf[k] for k in [1, 2, 3, 4, 5, 6, 7, 8, 9]])

    # Calculate Benford's law CDF ##############################################
    benfcdf = benfords().cdf
    npbenfcdf = np.array([benfcdf[k] for k in [1, 2, 3, 4, 5, 6, 7, 8, 9]])

    # Calculate input firstdigits PDF ##########################################
    firstdigitsN = firstdigits.size

    firstdigitspdf = np.bincount(firstdigits)
    firstdigitspdf = list(firstdigitspdf[1:] / firstdigitsN)

    # Calculate input firstdigits CDF ##########################################
    firstdigitscdf = []
    for k in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
        firstdigitscdf += [sum(firstdigitspdf[0:k])]

    # Calculate test value #####################################################
    if testtype == "Kuiper":
        Dplus = np.abs(np.max(np.subtract(npbenfcdf, firstdigitscdf)))
        Dminus = np.abs(np.max(np.subtract(firstdigitscdf, npbenfcdf)))

        V = Dplus + Dminus
        testvalue = V

    elif testtype == "KS":
        D = np.max(np.abs(np.subtract(npbenfcdf, firstdigitscdf)))
        D *= 3  # = sqrt(9)
        testvalue = D

    elif testtype == "m":
        maxPr = 0

        for idx, Pr in enumerate(firstdigitspdf):
            if Pr > maxPr:
                maxPr = Pr
                maxdigit = idx + 1

        m = firstdigitsN ** (1 / 2) * abs(maxPr - benfpdf[maxdigit])
        testvalue = m

    elif testtype == "d":
        summed = 0
        for idx, Pr in enumerate(firstdigitspdf):
            summed += (Pr - benfpdf[idx + 1]) ** 2

        d = (firstdigitsN * summed) ** (1 / 2)
        testvalue = d

    # Plot results #############################################################
    if plot is True:
        mptlib.plot([1, 2, 3, 4, 5, 6, 7, 8, 9],
                    npbenfpdf,
                    'b-',
                    label='Benford\'s law'
                    )
        mptlib.plot([1, 2, 3, 4, 5, 6, 7, 8, 9],
                    firstdigitspdf,
                    '-ro',
                    label='Sample data'
                    )
        mptlib.xlabel('first digit')
        mptlib.ylabel('probability')
        mptlib.title(testname[testtype] + ' ' + 'Test')
        mptlib.grid(True)
        mptlib.legend(loc='best',
                      title=testvar[testtype] +
                      ' = ' + '{:.4f}'.format(testvalue)
                      )
        mptlib.show(block=False)

    # Print significance #######################################################

    if printsignificance is True:
        significance = testsig(testtype, testvalue)
        print("Alpha  Significant?")
        print("-----  ------------")
        for alpha in sorted(significance.keys()):
            print("{:1.2f}   {}".format(alpha, significance[alpha]))

    return testvalue


def testsig(testtype, testvalue):
    """
    Tests whether test value is significant. Returns a dictionary with keys
    equal to alpha values and values as Boolean of whether test value is
    statistically significant. That is, if testvalue is significant at some
    significance level, the null hypothesis that the distribution follows
    Benford's law is rejected.

    :testtype:
    For "Kuiper", calculates whether Kuiper's test value V is significant for
    levels for alpha = 0.10. 0.05, and 0.01 based on [2010 Morrow].
    For "KS", calculates whether the Kolmogorov-Smirnov test value D is
    significant for levels for alpha = 0.10. 0.05, and 0.01 based on
    [2010 Morrow].
    For "m", calculates whether Leemis' m test value m is significant for
    levels for alpha = 0.10. 0.05, and 0.01 based on [2010 Morrow].
    For "d", calculates whether Cho-Gaines' d test value d is significant for
    levels for alpha = 0.10. 0.05, and 0.01 based on [2010 Morrow].

    :return: Returns dictionary of keys of alpha and values of whether test
    value is significant or not (T/F).
    """

    if testtype == "Kuiper":
        return {0.10: testvalue > 1.191,
                0.05: testvalue > 1.321,
                0.01: testvalue > 1.579}

    elif testtype == "KS":
        return {0.10: testvalue > 1.012,
                0.05: testvalue > 1.148,
                0.01: testvalue > 1.420}

    elif testtype == "m":
        return {0.10: testvalue > 0.851,
                0.05: testvalue > 0.967,
                0.01: testvalue > 1.212}

    elif testtype == "d":
        return {0.10: testvalue > 1.212,
                0.05: testvalue > 1.330,
                0.01: testvalue > 1.569}


def magnitudebin(data):
    """
    Calculates the orders of magnitudes of the data, returning them as
    a structured array with an index of the orders of magnitude in
    the data. As the number of significant digits in the fractional part
    of a number is lost, only the order of magnitude of the integer part
    is calculated here. If a datum is 0, assume it represents one order
    of magnitude.

    :param data: A 1D numpy array containing numbers.

    :return: A structured array with indices of the magnitude of the
    data numbers.
    """

    # A value of 0 will cause exception using log10 to calculate magnitude.
    # Set those data to 1 so they will result in a magnitude of 1.

    datanz = data
    datanz[datanz == 0] = 1
    magnitudes = np.around(np.log10(np.absolute(datanz)))
    magnitudes = magnitudes.astype(int)

    bin = np.bincount(magnitudes)

    orders = np.arange(len(bin))

    magnitudebin = dict(zip(orders, bin))

    return magnitudebin

