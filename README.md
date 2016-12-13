# Overview of Benford's Law

Benford's law is an empirically observed phenomenon where the first significant digit of sets of
numerical data follow a logarithmic distribution. Smaller digits such as one are more frequent as
the first digit than larger numbers such as nine. It discovery (in 1881 by 
[Simon Newcomb](https://en.wikipedia.org/wiki/Simon_Newcomb) and in 1938 by 
[Frank Benford](https://en.wikipedia.org/wiki/Frank_Benford)) came from the observation that 
logarithm tables appeared to be more worn for number starting with smaller digits. A good background
is found [here](https://en.wikipedia.org/wiki/Benford%27s_law). 

The conformity of numbers to Benford's law is, then, a sort of test of the quality of the underlying 
dataset. It has been used largely as a tool to detect fraud in forensic accounting, election results,
macroeconomic data, etc. but also to help assess the quality of scietific data (e.g., see
[here](http://www.checkyourdata.com/index.php)).

Note that there are apparently many subtleties to applying Benford's law. For example, the set of 
numbers should extend multiple orders of magnitude, so that that occurrence of smaller and larger digits
are well represented. Parts of datasets which are artificially restricted (e.g., a preference to 
purchase at $x.99 prices) will skew the observed distribution, although those are essentially just acts 
of "fraud" without the nefarious intent and can be detected just as well. As the analysis relies on a 
cumulative count, analyzing large datasets may not necessarily be advantageous: small subsets of 
fraud would become lost in the much larger set. It may be more effective to analyze smaller chunks
of data.

To the last two points about filtering out artificially restricted numbers and applying the analysis to 
whole vs smaller subsets of data, it implies an importance in being able to conscously filter data before 
applying the statistical analysis, to be discussed below in what should be inluded in the code.

Finally, there are several proposed tests for determining the significance of an observed distribution
of leading significant digits. Some have been implemented and more will be added.

# Overview of package

This package is a set of tools for applying Benford's law analysis, in early but otherwise working form 
(alpha?).

It should be able to perform the following:

* Access a variety of data sources, such as an SQL database, an Excel file, or a website.
* Parse / filter that data to create a set of numbers to analyze.
* Analyze a Benford's law analysis and determine the statistical significance.

In its current form, it can check for statistical significance using the following tests and test values,
which are from [Maddow](http://www.johnmorrow.info/projects/benford/benfordMain.pdf).

* Kuiper's test
* Kolmogorov-Smirnov's test
* Leemis' (et al.) test
* Cho and Gaines' test

Their significance test values are:

| Test Statistic | &#945; = 0.10 | &#945; = 0.05 | &#945; = 0.01 |
| ---            | ---           | ---           | ---           |
| Kuiper         | 1.191         | 1.321         | 1.579         |
| K-S            | 1.012         | 1.148         | 1.420         |
| Leemis et al.  | 0.851         | 0.967         | 1.212         |
| Cho and Gaine  | 1.212         | 1.330         | 1.569         |

Data can be passed in directly as a Python list of numbers. Data can also be loaded in from a
.xlsx Excel worksheet, filtered by sheet names, row and column identifiers, and specific ranges of
cells.

# Examples

## Excel

An Excel worksheet can be analyzed by creating a BenfordsPy object and running the analyzeexcel function:

```python
import BenfordsPy as BP

test = BP.BenfordsPy()
test.analyzeexcel('data.xlsx',
                  testtype="KS",
                  )
```

Note that a filename is required, followed by the type of significance test to be applied. Currently, either
"Kuiper" or "KS" can be used, which are the Kuiper's and Kolomogorov-Smirnov tests, respectively.

A plot (which uses Matplotlib) can be generated to view the results:

```python
import BenfordsPy as BP

test = BP.BenfordsPy()
test.analyzeexcel('data.xlsx',
                  testtype="KS",
                  plottest=True
                  )
```

The significance of the result can be printed:

```python
import BenfordsPy as BP

test = BP.BenfordsPy()
test.analyzeexcel('data.xlsx',
                  testtype="KS",
                  printsignificance=True
                  )
```

Data filtering is available by worksheet name and row/column names.

* Worksheet names: The name(s) of worksheets to be included must be explcitly included if 
they are to contribute to the data. This is a list of strings, such as {"Data1"}.

* Row and column labels: The cells to be included can be filtered by strings in the worksheet. If a row
containing Assets is desired, the string "Assets" can be included so that any rows/columns that
include that string *anywhere* in that row/column (exact and case-sensitive) will contribute to the analysis.
Rows/columns can be both included and excluded, and have a flag for inclusion by default if a row/column 
label is not expicitly included or excluded.

Note that a row/column is included if it is not in the exclude list and it is either in the include list
or the default inclusion flag is true. So if a row/column name is in both the inclusion and exclusion
lists, it will be included or excluded based on the default inclusion flag.

The flag for default inclusion for rows is true but for columns is false.

To exclude the Sheet1 and Sheet2 worksheets, include all rows except Assets:
```python
import BenfordsPy as BP

test = BP.BenfordsPy()
test.analyzeexcel('data.xlsx',
                  testtype="KS",
                  wkshtincl={"Sheet1", "Sheet2"},
                  rowlblexcl={"Assets"},
                  rowlblincldefault=True
                  )
```

Similar sets of strings can be passed on for rowblincl, and their respective variables for columns
collblincl, collblexcl, and collbluncldefault.
			  

# To do:

* Add more significance tests and check existing statistical tests.
* Add web interface.
* Incorporate regular expressions to data filtering.
* Incororate filtering by cell ranges.