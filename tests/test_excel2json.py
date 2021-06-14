"""Collection of tests around log handling."""
import logging
import unittest
from logger import configure_logger
from excel2json import excel2json
from version import NAME


class testExcel2json(unittest.TestCase):

    # {
    # "Sheet": {
    #     "1": {
    #         "Column1": "row1"
    #     },
    #     "2": {
    #         "Column1": "row2"
    #     }
    # }


    def setUp(self):

        self.hash = {
            "1": {
                "Column1": "row1"
            },
            "2": {
                "Column1": "row2"
            }
        }

    # def test_init_logging_info(self):
    #     """ Test init logging with level info"""
    #     with self.assertLogs(NAME, level='INFO') as lc:
    #         self.form = excel2json("library/example.xls")
    #         self.assertEqual([], lc.output)

    def test_init_logging_debug(self):
        """ Test init logging with level debug"""
        with self.assertLogs(NAME, level='DEBUG') as lc:
            self.form = excel2json("tests/test.xls")
            self.assertEqual([f"DEBUG:{NAME}:Pass in excel2json.init()"],lc.output)

    def test_worksheet_name(self):
        """ Test the worksheet name = sheet """
        self.form = excel2json("tests/test.xls")
        self.assertEqual(['Sheet'], self.form.worksheets)

    def test_3_worksheet_values(self):
        ''' Test default values in Excel test.xls'''
        self.form = excel2json("tests/test.xls")
        h = self.form.toDict()
        d = h['Sheet']
        for k in d.keys():
            self.assertEqual(d[k], self.hash[k])

    # add write test.json, remove file, add and delete values

if __name__ == '__main__':
    unittest.main()
