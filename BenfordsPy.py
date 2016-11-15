"""
Run Benford's Law analysis of data.
"""

from excel import ExcelDB
import numerics
import dataset

class BenfordsPy:

    def __init__(self):
        self.result = 0

    def analyzeexcel(self,
                     filename,
                     testtype,
                     wkshtincl=None,
                     rowlblincl=None,
                     rowlblexcl= None,
                     rowlblincldefault=None,
                     collblincl= None,
                     collblexcl= None,
                     collblincldefault=None,
                     celrngincl= None,
                     celrngexcl= None,
                     celrngincldefault=None,
                     plottest=False,
                     printsignificance=False
                     ):
        """
        Analyze data from Excel file.

        :param filename:
        :return:
        """

        db = ExcelDB(filename)
        data = dataset.dataset()

        if wkshtincl and isinstance(wkshtincl, set):
            db.Filter.WorkSheets.include = wkshtincl

        if rowlblincl and isinstance(rowlblincl, set):
            db.Filter.RowLabels.include = rowlblincl
        if rowlblexcl and isinstance(rowlblexcl, set):
            db.Filter.RowLabels.exclude = rowlblexcl
        if rowlblincldefault:
            db.Filter.RowLabels.defaultinclude = rowlblincldefault

        if collblincl and isinstance(collblincl, set):
            db.Filter.ColLabels.include = collblincl
        if collblexcl and isinstance(collblexcl, set):
            db.Filter.ColLabels.exclude = collblexcl
        if collblincldefault:
            db.Filter.ColLabels.defaultinclude = collblincldefault

        if celrngincl and isinstance(collblincl, set):
            db.Filter.CellRange.include = celrngincl
        if celrngexcl and isinstance(celrngexcl, set):
            db.Filter.CellRange.exclude = celrngexcl
        if celrngincldefault:
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

