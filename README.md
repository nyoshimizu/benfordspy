## Overview

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
cumulative count, analyzing whole, large datasets may not necessarily be advantageous. Small subsets of 
fraud would become lost in the much larger set. 

To the last two points about filtering out artificially restricted numbers and applying the analysis to 
whole vs smaller subsets of data, it implies an importance in being able to conscously filter data before 
applying the statistical analysis, to be discussed below in what should be inluded in the code.



This is a set of tools for applying Benford's law analysis. 

It should be able to perform the following:

* Access a variety of data sources, such as an SQL database, an Excel file, or a website.
* Parse / filter that data to create a set of number s