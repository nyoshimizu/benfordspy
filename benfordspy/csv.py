"""
This class accesses data from CSV files.
"""

import numpy as np


class CSVDB:

    def __init__(self, file):
        self.CSV_data = np.genfromtxt(file, delimiter=',')

    class Filter:
        """
        This class holds the filters applied to the CSV data to determine
        the numbers that will be passed on for the Benford Law's test.
        There are three parameters: row labels, column labels, worksheets, and
        cell range.
        Note that a parameter is used if it is in the include list and not used
        if it is in the exclude list. If neither, the defaultinclude parameter
        will be used to determine whether or not to use the parameter. Ranges
        which are mistakenly both in the include and exclude lists will default
        to the defaultinclude setting.
        Row and column labels are strings, and are applied to any cell within
        the row or column.
        All matches are exact, including string case.
        """

        class RowLabels:

            include = set()
            exclude = set()

            defaultinclude = False

        class ColLabels:

            include = set()
            exclude = set()

            defaultinclude = False

        class RowNumbers:
            include = set()
            exclude = set()

            defaultinclude = False

        class ColNumbers:
            include = set()
            exclude = set()

            defaultinclude = False

    def extractnumbers(self):
        """
        Apply the filters set in the Filter class and return the set of all
        numbers from the CSV file.

        :return: List of numbers from CSV file subject to Filter.
        """

        datareturn = []

        # Filter rows
        rows = []
        for row_idx, row_entry in enumerate(self.CSV_data):
            ifincl = any(
                         (set(row_entry) & self.Filter.RowLabels.include)
                         |
                         ({row_idx} & self.Filter.RowNumbers.include)
                         )
            ifexcl = any(
                         (set(row_entry) & self.Filter.RowLabels.exclude)
                         |
                         ({row_idx} & self.Filter.RowNumbers.exclude)
                         )
            ifdefault = (
                         self.Filter.RowLabels.defaultinclude
                         |
                         self.Filter.RowNumbers.defaultinclude
                         )

            if ifexcl is False and any((ifincl, ifdefault)):
                rows += [row_idx]

        # Filter columns
        CSV_data_transpose = np.transpose(self.CSV_data)
        columns = []
        for col_idx, col_entry in enumerate(CSV_data_transpose):
            ifincl = any(
                         (set(col_entry) & self.Filter.ColLabels.include)
                         |
                         ({col_idx} & self.Filter.ColNumbers.include)
                         )
            ifexcl = any(
                         (set(col_entry) & self.Filter.ColLabels.exclude)
                         |
                         ({col_idx} & self.Filter.ColNumbers.exclude)
                         )
            ifdefault = (
                         self.Filter.ColLabels.defaultinclude
                         |
                         self.Filter.ColNumbers.defaultinclude
                         )

            if ifexcl is False and any((ifincl, ifdefault)):
                columns += [col_idx]

        # Extract data from CSV data
        maskrow = np.zeros(self.CSV_data.shape)
        for rw in rows:
            maskrow[rw, :] = 1

        maskcol = np.zeros(self.CSV_data.shape)
        for cl in columns:
            maskcol[:, cl] += 1

        mask = np.multiply(maskrow, maskcol)

        # Apply mask
        CSV_data_numbers = np.ma.array(self.CSV_data, mask=np.logical_not(mask))
        # Remove NaN's
        CSV_data_numbers = CSV_data_numbers[~np.isnan(CSV_data_numbers)]
        # Flatten
        CSV_data_numbers = CSV_data_numbers.flatten()
        # Convert to list
        CSV_data_numbers = CSV_data_numbers.tolist()
        # Remove None and 0
        CSV_data_numbers = [number for number in CSV_data_numbers
                            if number is not None and number is not 0]

        datareturn = CSV_data_numbers

        return datareturn