"""
Run Benford's Law analysis of data.
"""

from benfordspy.excel import ExcelDB
import benfordspy.numerics as numerics
import benfordspy.dataset as dataset


class BenfordsPy:

    def __init__(self):
        self.result = 0

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

        if testtype == "Kuiper":
            self.result = numerics.kuipertest(data.firstdigits, plot=plottest)
            print("Kuiper's test value V = {:.4f}".format(self.result))
            if printsignificance:
                significance = numerics.kuipertestsig(self.result)
                print("Alpha  Significant?")
                print("-----  ------------")
                for alpha in sorted(significance.keys()):
                    print("{:1.2f}   {}".format(alpha, significance[alpha]))

        if testtype == "KS":
            self.result = numerics.kstest(data.firstdigits, plot=plottest)
            print("Kolmogorov-Smirnov test value D = {:.4f}".format(self.result))
            if printsignificance:
                significance = numerics.kstestsig(self.result)
                print("Alpha  Significant?")
                print("-----  ------------")
                for alpha in sorted(significance.keys()):
                    print("{:1.2f}   {}".format(alpha, significance[alpha]))

        if testtype == "m":
            self.result = numerics.mtest(data.firstdigits, plot=plottest)
            print("Leemis' m test value m = {:.4f}".format(self.result))
            if printsignificance:
                significance = numerics.mtestsig(self.result)
                print("Alpha  Significant?")
                print("-----  ------------")
                for alpha in sorted(significance.keys()):
                    print("{:1.2f}   {}".format(alpha, significance[alpha]))

        if testtype == "d":
            self.result = numerics.dtest(data.firstdigits, plot=plottest)
            print("Cho-Gaines' s test value d = {:.4f}".format(self.result))
            if printsignificance:
                significance = numerics.dtestsig(self.result)
                print("Alpha  Significant?")
                print("-----  ------------")
                for alpha in sorted(significance.keys()):
                    print("{:1.2f}   {}".format(alpha, significance[alpha]))
