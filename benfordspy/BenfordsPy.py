"""
Run Benford's Law analysis of data.
"""

from benfordspy.excel import ExcelDB
from benfordspy.csv import CSVDB
import benfordspy.numerics as numerics
import benfordspy.dataset as dataset


class BenfordsPy:

    def __init__(self):
        self.result = 0

    def dotest(self,
               data,
               testtype,
               plottest=False,
               printsignificance=False
               ):

        self.result = numerics.test(testtype,
                                    data.firstdigits,
                                    plottest,
                                    printsignificance)

    def analyzelist(self,
                    input,
                    testtype,
                    plottest=False,
                    printsignificance=False
                    ):
        """
        Analyze data from input list of numbers.

        :param data: 1-D list of numbers to analyze.
        :param testtype: Test of significance to apply.
        :param plottest: Flag to plot results; default value is False.
        :param printsignificance: Flag to output significance test results;
        default is False.

        :return: Nothing.
        """
        if not isinstance(input, list):
            raise TypeError("Input to analyzelist is not a list.")

        for element in input:
            if not isinstance(element, (int, float)):
                raise TypeError("Input to analyzelist contains non-int or" +
                                "non-float element.")

        data = dataset.dataset()
        data.datainit(input)
        data.updatefirstdigits()

        self.result = numerics.test(testtype,
                                    data.firstdigits,
                                    plottest,
                                    printsignificance
                                    )

    def analyzeexcel(self,
                     filename,
                     testtype,
                     wkshtincl=None,
                     rowlblincl=None,
                     rowlblexcl=None,
                     rowlblincldefault=False,
                     collblincl=None,
                     collblexcl=None,
                     collblincldefault=True,
                     celrngincl=None,
                     celrngexcl=None,
                     celrngincldefault=True,
                     plottest=False,
                     printsignificance=False
                     ):
        """
        Analyze data from Excel file.

        :param filename: Excel file.
        :param testtype: Test of significance to apply.
        :param wkshtincl: Set of worksheet names to include.
        :param rowlblincl: Set of row labels to include.
        :param rowlblexcl: Set of row labels to exclude.
        :param rowlblincldefault: Flag to include rows by default; default value
        is True.
        :param collblincl: Set of column labels to include.
        :param collblexcl: Set of column labels to exclude.
        :param collblincldefault: Flag to include column by default; default
        value is False.
        :param celrngincl: Set of cell ranges to include.
        :param celrngexcl: Set of cell ranges to exclude.
        :param celrngincldefault: Flag to include cell ranges by default;
        default value is True.
        :param plottest: Flag to plot results; default value is False.
        :param printsignificance: Flag to output significance test results;
        default is False.

        :return: Nothing.
        """

        db = ExcelDB(filename)
        data = dataset.dataset()

        if wkshtincl and isinstance(wkshtincl, set):
            db.Filter.WorkSheets.include = wkshtincl

        if rowlblincl and isinstance(rowlblincl, set):
            db.Filter.RowLabels.include = rowlblincl
        if rowlblexcl and isinstance(rowlblexcl, set):
            db.Filter.RowLabels.exclude = rowlblexcl
        db.Filter.RowLabels.defaultinclude = rowlblincldefault

        if collblincl and isinstance(collblincl, set):
            db.Filter.ColLabels.include = collblincl
        if collblexcl and isinstance(collblexcl, set):
            db.Filter.ColLabels.exclude = collblexcl
        db.Filter.ColLabels.defaultinclude = collblincldefault

        if celrngincl and isinstance(collblincl, set):
            db.Filter.CellRange.include = celrngincl
        if celrngexcl and isinstance(celrngexcl, set):
            db.Filter.CellRange.exclude = celrngexcl
        db.Filter.CellRange.defaultinclude = celrngincldefault

        exceldata = db.extractnumbers()
        data.datainit(exceldata)
        if data.data.size == 0:
            raise IOError("Loaded no data, quitting")

        data.updatefirstdigits()

        self.result = numerics.test(testtype,
                                    data.firstdigits,
                                    plottest,
                                    printsignificance
                                    )

    def analyzeCSV(self,
                   filename,
                   testtype,
                   rowlblincl=None,
                   rowlblexcl=None,
                   rowlblincldefault=False,
                   collblincl=None,
                   collblexcl=None,
                   collblincldefault=False,
                   rownumincl=None,
                   rownumexcl=None,
                   rownumincldefault=False,
                   colnumincl=None,
                   colnumexcl=None,
                   colnumincldefault=False,
                   plottest=False,
                   printsignificance=False
                   ):
        """
        Analyze data from Excel file.

        :param filename: Excel file.
        :param testtype: Test of significance to apply.
        :param rowlblincl: Set of row labels to include.
        :param rowlblexcl: Set of row labels to exclude.
        :param rowlblincldefault: Flag to include rows by default; default value
        is False.
        :param collblincl: Set of column labels to include.
        :param collblexcl: Set of column labels to exclude.
        :param collblincldefault: Flag to include column by default; default
        value is False.
        :param rownumincl: Set of row numbers to include.
        :param rownumexcl: Set of row numbers  to exclude.
        :param rownumincldefault: Flag to include row numbers by default;
        default value is False.
        :param colnumincl: Set of column numbers to include.
        :param colnumexcl: Set of column numbers  to exclude.
        :param colnumincldefault: Flag to include column numbers by default;
        default value is False.
        :param plottest: Flag to plot results; default value is False.
        :param printsignificance: Flag to output significance test results;
        default is False.

        :return: Nothing.
        """

        db = CSVDB(filename)
        data = dataset.dataset()

        if rowlblincl and isinstance(rowlblincl, set):
            db.Filter.RowLabels.include = rowlblincl
        if rowlblexcl and isinstance(rowlblexcl, set):
            db.Filter.RowLabels.exclude = rowlblexcl
        db.Filter.RowLabels.defaultinclude = rowlblincldefault

        if collblincl and isinstance(collblincl, set):
            db.Filter.ColLabels.include = collblincl
        if collblexcl and isinstance(collblexcl, set):
            db.Filter.ColLabels.exclude = collblexcl
        db.Filter.ColLabels.defaultinclude = collblincldefault

        if rownumincl and isinstance(rownumincl, set):
            db.Filter.RowNumbers.include = rownumincl
        if rownumexcl and isinstance(rownumexcl, set):
            db.Filter.RowNumbers.exclude = rownumexcl
        db.Filter.RowNumbers.defaultinclude = rownumincldefault

        if colnumincl and isinstance(colnumincl, set):
            db.Filter.ColNumbers.include = colnumincl
        if colnumexcl and isinstance(colnumexcl, set):
            db.Filter.ColNumbers.exclude = colnumexcl
        db.Filter.ColNumbers.defaultinclude = colnumincldefault

        CSVdata = db.extractnumbers()

        data.datainit(CSVdata)
        if data.data.size == 0:
            raise IOError("Loaded no data, quitting")

        data.updatefirstdigits()

        self.result = numerics.test(testtype,
                                    data.firstdigits,
                                    plottest,
                                    printsignificance
                                    )
