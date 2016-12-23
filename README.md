# Overview of Benford's Law

Benford's law is an empirically observed phenomenon where the first significant digit of sets of
numerical data follow a logarithmic distribution. Smaller digits such as one are more frequent as
the first digit than larger numbers such as nine. It discovery (in 1881 by 
<a href="https://en.wikipedia.org/wiki/Simon_Newcomb" target="_blank">Simon Newcomb</a> and in 1938 by
<a href="https://en.wikipedia.org/wiki/Frank_Benford" target="_blank">Frank Benford</a>) came from the
observation that logarithm tables appeared to be more worn for number starting with smaller digits. A
good background is found at <a href="https://en.wikipedia.org/wiki/Benford%27s_law" target="_blank">Wikipedia</a>.
Terrence Tao discusses
<a href="https://terrytao.wordpress.com/2009/07/03/benfords-law-zipfs-law-and-the-pareto-distribution/"
target="_blank">here</a> how scale invariance is important in understanding the origin of this distribution.

The conformity of numbers to Benford's law is, then, a sort of test of the quality of the underlying 
dataset. It has been used largely as a tool to detect fraud in forensic accounting, election results,
macroeconomic data, etc. but also to help assess the quality of scietific data (e.g., see
<a href="http://www.checkyourdata.com/index.php" target="_blank">here</a>).

Note that there are apparently many subtleties to applying Benford's law. For example, the set of 
numbers should extend multiple orders of magnitude, so that that occurrence of smaller and larger digits
are well represented. Parts of data sets which are artificially restricted (e.g., a preference to
purchase at $x.99 prices) will skew the observed distribution, although those are essentially just acts 
of "fraud" without the nefarious intent and can be detected just as well. As the analysis relies on a 
cumulative count, analyzing large data sets may not necessarily be advantageous: small subsets of
fraud would become lost in the much larger set. It may be more effective to analyze smaller chunks
of data.

To the last two points about filtering out artificially restricted numbers and applying the analysis to 
whole vs subsets of data, it implies an importance in deliberately filtering data before
applying the statistical analysis. This is to be discussed below in what capabilities the package should have.

Finally, there are several proposed tests for determining the significance of an observed distribution
of leading significant digits. They are also discussed below.

# Overview of package

This package is a set of tools for applying Benford's law analysis, in early but otherwise working form.

It should be able to perform the following:

* Access a variety of data sources, such as an SQL database, an Excel file, a website, or most simply a list.
* Parse / filter that data to create a set of numbers to analyze.
* Apply a Benford's law analysis and determine the statistical significance.

In its current form, it can check for statistical significance using the following tests and test values,
which are from Morrow<sup>[1](#Morrow)</sup>.

1. <a href="https://en.wikipedia.org/wiki/Kuiper's_test" target="_blank">Kuiper's test</a>
2. <a href="https://en.wikipedia.org/wiki/Kolmogorov%E2%80%93Smirnov_test" target="_blank">Kolmogorov-Smirnov's test</a>
3. Modified Leemis' (et al.) d test<sup>[2](#Leemis)</sup>
4. Modified Cho and Gaines' m test<sup>[3](#Cho-Gaines)</sup>

Their significance test values are:

| Test Statistic   | &#945; = 0.10 | &#945; = 0.05 | &#945; = 0.01 |
| ---              | ---           | ---           | ---           |
| 1. Kuiper        | 1.191         | 1.321         | 1.579         |
| 2. K-S           | 1.012         | 1.148         | 1.420         |
| 3. Leemis et al. | 0.851         | 0.967         | 1.212         |
| 4. Cho and Gaines| 1.212         | 1.330         | 1.569         |

Data can be passed in directly as a Python list of numbers. Data can also be loaded from a
.xlsx Excel worksheet, filtered by sheet names, row and column identifiers, and specific ranges of
cells.

# Usage

## Parameters

These are the parameters that set the analysis.

* *testtype*: A number of significance tests are available, as described above. They are set using the *testtype*
parameter, and can be set to "Kuiper," "KS," "m," or "d," the latter two corresponding to Leemis' and Cho and Gaines'
tests, respectively.
* *plottest*: This flag, when True, will generate a plot to view the results using Matplotlib.
* *printsignificance*: This flag, when True, will print the results of the significance test to the output.

Filtering is done by labels or row/column numbers. Labels are strings that exist anywhere in that row or column.
Row/columns can be included or excluded based on either strings or their number: e.g., include all rows that have
the string "Profit" in them or exclude columns three to six.

Each of these also has a default include flag, for example include all row numbers by default or include all
column labels by default. Then, exclusions can be provided so that e.g. all row numbers except six to seven are
included or all column labels except "Balance Sheet" are included. By default, all the default include flags are
False so at least one for both row and column must be enabled, or specific rows or labels must be included; otherwise,
no data will be loaded.

Usage can be seen in the examples below.

## Direct analysis

A list of numerical values can be directly analyzed:

```python
import benfordspy.BenfordsPy as BP

mydata = [1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 4, 4, 5, 5, 6, 7, 7, 8, 9]
test = BP.BenfordsPy()
test.analyzelist(mylist,
                 testtype="Kuiper",
                 rowlblincldefault=True,
                 collblincldefault=True
                 )
```

## Excel

An Excel worksheet can be analyzed by creating a BenfordsPy object and running its analyzeexcel method:

```python
import BenfordsPy as BP

test = BP.BenfordsPy()
test.analyzeexcel('data.xlsx',
                  testtype="KS",
                  rowlblincldefault=True,
                  collblincldefault=True
                  )
```

Note that it requires a filename and the type of significance test to be applied.

Data filtering is available by worksheet name and row/column names.

* Worksheet names: The name(s) of worksheets to be included must be explicitly included if
they are to contribute to the data. This is a set of strings, such as {"Sheet1", "Sheet2"}.
* Row and column labels: The cells to be included can be filtered by strings in the worksheet. If a row
containing "Assets" is desired, the string "Assets" can be included so that any rows/columns that
include that string anywhere in that row/column (exact and case-sensitive) will contribute to the analysis.
Rows/columns can be both included and excluded. There is also a flag for inclusion by default, used for cases where
a row/column label is not explicitly included or excluded.
* Cell ranges: not implemented.

Note that a row/column is included if it is not in the exclude list, and it is in the include list
or the default inclusion flag is true. So if a row/column name is in both the inclusion and exclusion
lists (presumably a mistake), it will be included or excluded based on the default inclusion flag.

To include the Sheet1 and Sheet2 worksheets, include all rows except "Assets," and display all the results:

```python
import BenfordsPy as BP

test = BP.BenfordsPy()
test.analyzeexcel('data.xlsx',
                  testtype="KS",
                  wkshtincl={"Sheet1", "Sheet2"},
                  rowlblincldefault=True,
                  rowlblexcl={"Assets"},
                  collblincldefault=True,
                  plottest=True,
                  printsignificance=True
                  )
```

Similar sets of strings can be passed on for *rowblincl*, and their respective variables for columns
*collblincl*, *collblexcl*, and *collblincldefault*.

## CSV

A CSV file can be analyzed by creating a BenfordsPy object and running its analyzeCSV method:

```python
import BenfordsPy as BP

test = BP.BenfordsPy()
test.analyzeCSV('data.csv',
                testtype="KS",
                rowlblincldefault=True,
                collblincldefault=True
                )
```

Note that it requires a filename and the type of significance test to be applied.

Data filtering is available by row/column names and row/column numbers.

* Row and column labels: The values to be included can be filtered by strings in the worksheet. If a row
containing "Assets" is desired, the string "Assets" can be included so that any rows/columns that
include that string anywhere in that row/column (exact and case-sensitive) will contribute to the analysis.
Rows/columns can be both included and excluded. There is also a flag for inclusion by default, used for cases where
a row/column label is not explicitly included or excluded.
* Row and column numbers: Specific row/columns can be included by number.

Note that a row/column is included if it is not in the exclude list, and it is in the include list
or the default inclusion flag is true. So if a row/column name is in both the inclusion and exclusion
lists (presumably a mistake), it will be included or excluded based on the default inclusion flag.

```python
import BenfordsPy as BP

test = BP.BenfordsPy()
test.analyzeCSV('data.csv',
                testtype="KS",
                rowlblincldefault=True,
                colnumincl={3, 4, 5, 6},
                plottest=True,
                printsignificance=True
                )
```

# To do:

* Add interface for XML, JSON.
* Add web / scraping interface.
* Incorporate some sort of automated subset analysis.
* Incorporate regular expressions to data filtering.
* Incorporate filtering by cell ranges of Excel files.
* Parse dates as well (?).

# References

<a name="Morrow"> [1] Morrow, J., "<a href="http://cep.lse.ac.uk/pubs/download/dp1291.pdf" target="_blank">Benford's law, families of distributions and a test basis</a>,"
Center for Economic Performance, London School of Economics, CEP discussion paper 1291,  2014.</a>

<a name="Leemis"> [2] Leemis, L. M., Schmeiser, B. W., and Evans, D. L., "Survival distributions satisfying Benford's Law," *The American
Statistician*, **54**, pp. 236&mdash;41, 2000. </a>

<a name="Cho-Gaines"> [3] Cho, W. K. T., and Gaines, B. J., "Breaking the (Benford) law: statistical fraud detection in campaign finance,"
*The American Statistician*, **61**, pp. 218&mdash;33, 2007.