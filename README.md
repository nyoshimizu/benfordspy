# Overview

Benford's law is an empirically observed phenomenon where the first significant digit of sets of
numerical data follow a logarithmic distribution. Smaller digits such as one are more frequent as
the first digit than larger numbers such as nine. It discovery (in 1881 by 
[Simon Newcomb](https://en.wikipedia.org/wiki/Simon_Newcomb) and in 1938 by 
[Frank Benford](https://en.wikipedia.org/wiki/Frank_Benford)) came from the observation that 
logarithm tables appeared to be more worn for number starting with smaller digits. A good background
is found [here](https://en.wikipedia.org/wiki/Benford%27s_law). 

The conformity of numbers to Benford's law is, then, a sort of test of the quality of the 

This is a set of tools for applying Benford's law analysis. 

```python
test = []
```

It should be able to perform the following:

* Access a variety of data sources, such as an SQL database, an Excel file, or a website.
* Parse / filter that data to create a set of number s