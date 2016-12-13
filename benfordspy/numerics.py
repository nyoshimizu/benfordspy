"""
This contains functions to perform some important numerical work.
"""

import numpy as np
import matplotlib.pyplot as mptlib


def kuipertest(firstdigits, plot=False):
    """
    Apply Kuiper's test to set of first digits from dataset. For cumulative
    distributions CDF1 and CDF2, which is a function of random variable
    x_i (i = 1,..n).
    Then

    D+ = max[CDF2(x_i) - CDF1(x_i)]
    D- = max[CDF1(x_i) - CDF2(x_i)]

    and the test statistic V = D+ + D-, using positive distances D+ and D-.

    :param firstdigits: Numpy array of ints containing first digits from
    dataset.
    :param plot: Flag for plotting results.

    :return: Return Kuiper test statistic V.
    """

    # Calculate Benford's law CDF ##############################################
    benfpdf = []

    for k in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
        benfpdf += [benfords(k)]

    assert sum(benfpdf) == 1

    benfcdf = []

    for k in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
        benfcdf += [sum(benfpdf[0:k])]

    assert benfcdf[-1] == 1

    benfcdf = np.array(benfcdf)

    # Calculate input firstdigits CDF ##########################################
    firstdigitsN = firstdigits.size

    firstdigitspdf = np.bincount(firstdigits)

    firstdigitspdf = list(firstdigitspdf[1:]/firstdigitsN)

    firstdigitscdf = []
    for k in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
        firstdigitscdf += [sum(firstdigitspdf[0:k])]

    firstdigitscdf = np.array(firstdigitscdf)

    # Calculate V value ########################################################
    Dplus = np.abs(np.max(np.subtract(benfcdf, firstdigitscdf)))

    Dminus = np.abs(np.max(np.subtract(firstdigitscdf, benfcdf)))

    V = Dplus + Dminus

    if plot is True:
        mptlib.plot([1, 2, 3, 4, 5, 6, 7, 8, 9],
                    benfcdf,
                    'b-',
                    label='Benford\'s law')
        mptlib.plot([1, 2, 3, 4, 5, 6, 7, 8, 9],
                    firstdigitscdf,
                    '-ro',
                    label='Sample data')
        mptlib.xlabel('first digit')
        mptlib.ylabel('cumulative probability')
        mptlib.title('Kuiper\'s Test')
        mptlib.grid(True)
        mptlib.legend(loc='best',
                      title='V = ' + '{:.4f}'.format(V.item())
                      )
        mptlib.show(block=False)

    return V


def kuipertestsig(V):
    """
    Calculates whether Kuiper's test value V is significant for levels for
    alpha = 0.10. 0.05, and 0.01 based on [2010 Morrow]. Returns a dictionary
    with keys equal to alpha values and values as Boolean of whether V is
    statistically significant. That is, if V is significant at some significance
    level, the null hypothesis that the distribution follows Benford's law
    is rejected.

    :param V: Kuiper's test value V

    :return: Dictionary with keys of significance levels 0.10, 0.05, 0.01 and
    Boolean values whether V is significant.
    """

    return {0.10: V > 1.191,
            0.05: V > 1.321,
            0.01: V > 1.579}


def kstest(firstdigits, plot=False):
    """
    Apply Kolmogorov-Smirnov test to set of first digits from dataset. For
    cumulative distributions CDF1 and CDF2, which is a function of random
    variable x_i (i = 1,..n).
    Then

    D = max[abs(CDF2(x_i) - CDF1(x_i))],

    that is, the maximum distance between CDF's.

    :param firstdigits: Numpy array of ints containing first digits from
    dataset.
    :param plot: Flag for plotting results.

    :return: Return Kuiper test statistic V.
    """
    # Calculate Benford's law CDF ##############################################
    benfpdf = []

    for k in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
        benfpdf += [benfords(k)]

    assert sum(benfpdf) == 1

    benfcdf = []

    for k in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
        benfcdf += [sum(benfpdf[0:k])]

    assert benfcdf[-1] == 1

    benfcdf = np.array(benfcdf)

    # Calculate input firstdigits CDF ##########################################
    firstdigitsN = firstdigits.size

    firstdigitspdf = np.bincount(firstdigits)

    firstdigitspdf = list(firstdigitspdf[1:]/firstdigitsN)

    firstdigitscdf = []
    for k in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
        firstdigitscdf += [sum(firstdigitspdf[0:k])]

    # Calculate D value ########################################################
    D = np.max(np.abs(np.subtract(benfcdf, firstdigitscdf)))

    D *= 3  # = sqrt(9)

    if plot is True:
        mptlib.plot([1, 2, 3, 4, 5, 6, 7, 8, 9],
                    benfcdf,
                    'b-',
                    label='Benford\'s law'
                    )
        mptlib.plot([1, 2, 3, 4, 5, 6, 7, 8, 9],
                    firstdigitscdf,
                    '-ro',
                    label='Sample data'
                    )
        mptlib.xlabel('first digit')
        mptlib.ylabel('cumulative probability')
        mptlib.title('Kolmogorov–Smirnov Test')
        mptlib.grid(True)
        mptlib.legend(loc='best',
                      title='D = ' + '{:.4f}'.format(D.item())
                      )
        mptlib.show(block=False)

    return D


def kstestsig(D):
    """
    Calculates whether the Kolmogorov-Smirnov test value D is significant for
    levels for alpha = 0.10. 0.05, and 0.01 based on [2010 Morrow]. Returns a
    dictionary with keys equal to alpha values and values as Boolean of whether
    V is statistically significant. That is, if V is significant at some
    significance level, the null hypothesis that the distribution follows
    Benford's law is rejected.

    :param D: Kolmogorov-Smirnov test value D

    :return: Dictionary with keys of significance levels 0.10, 0.05, 0.01 and
    Boolean values whether D is significant.
    """

    return {0.10: D > 1.012,
            0.05: D > 1.148,
            0.01: D > 1.420}


def mtest(firstdigits, plot=False):
    """
    Apply Leemis' m test based on [2010 Morrow]. The modified test statistic
    m*_N is defined as,

    m*_N = sqrt(N) * max {d=1..9} | Pr(X has X has FSD = d) - Benfords(d) |,

    where N is number of observations, First Significant Digit is d for the
    observations X, and Benfords is the Befords law for FSD = d, or
    log10(1+1/d).

    :param firstdigits: Numpy array of ints containing first digits from
    dataset.
    :param plot: Flag for plotting results.

    :return: Return m test statistic m.
    """

    PrX = []

    # Calculate Benford's law CDF ##############################################
    benfpdf = []

    for k in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
        benfpdf += [benfords(k)]

    assert sum(benfpdf) == 1

    benfcdf = []

    for k in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
        benfcdf += [sum(benfpdf[0:k])]

    assert benfcdf[-1] == 1

    benfcdf = np.array(benfcdf)

    # Calculate input firstdigits CDF ##########################################
    firstdigitsN = firstdigits.size

    firstdigitspdf = np.bincount(firstdigits)

    firstdigitspdf = list(firstdigitspdf[1:] / firstdigitsN)

    firstdigitscdf = []
    for k in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
        firstdigitscdf += [sum(firstdigitspdf[0:k])]

    # Calculate m value #########################################################
    maxPr = 0

    for idx, Pr in enumerate(firstdigitspdf):
        if Pr > maxPr:
            maxPr = Pr
            digit = idx+1

    m = firstdigitsN**(1/2)*abs(maxPr - benfords(digit))

    if plot is True:
        mptlib.plot([1, 2, 3, 4, 5, 6, 7, 8, 9],
                    benfcdf,
                    'b-',
                    label='Benford\'s law'
                    )
        mptlib.plot([1, 2, 3, 4, 5, 6, 7, 8, 9],
                    firstdigitscdf,
                    '-ro',
                    label='Sample data'
                    )
        mptlib.xlabel('first digit')
        mptlib.ylabel('cumulative probability')
        mptlib.title('Leemis\' m Test')
        mptlib.grid(True)
        mptlib.legend(loc='best',
                      title='m = ' + '{:.4f}'.format(m.item())
                      )
        mptlib.show(block=False)

    return m


def mtestsig(m):
    """
    Calculates whether Leemis' m test value m is significant for
    levels for alpha = 0.10. 0.05, and 0.01 based on [2010 Morrow]. Returns a
    dictionary with keys equal to alpha values and values as Boolean of whether
    m is statistically significant. That is, if V is significant at some
    significance level, the null hypothesis that the distribution follows
    Benford's law is rejected.

    :param m: Leemis' m test value m

    :return: Dictionary with keys of significance levels 0.10, 0.05, 0.01 and
    Boolean values whether D is significant.
    """

    return {0.10: m > 0.851,
            0.05: m > 0.967,
            0.01: m > 1.212}


def benfords(firstdigit):
    """
    Calculates, based on Benford's law, the probability that the leading digit
    is equal to firstdigit (1-9) in base 10.

    :param firstdigit: Numerical value of first digit of a number.

    :return: Benford's law probability of firstidigit as first digit of a
    number.
    """

    return np.log10(1+1/firstdigit)


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

