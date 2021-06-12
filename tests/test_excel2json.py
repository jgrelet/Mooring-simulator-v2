"""Collection of tests around log handling."""
import logging
import unittest
from logger import configure_logger
from excel2json import excel2json
from version import NAME


class testExcel2json(unittest.TestCase):

    #def setUp(self):

    def test_init_logging_info(self):
        """ Test init logging with level info"""
        with self.assertLogs(NAME, level='INFO') as lc:
            self.form = excel2json("library/example.xls")
            self.assertEqual([f"INFO:{NAME}:Pass in excel2json.init()"], lc.output)
            # self.sheet_names = self.form.worksheets
            # self.assertEqual(['ERROR: File size is 0 bytes, unable to open worksheet file'], lc.output)
            #self.sheet_names = self.form.worksheets
            #self.assertEqual(['DEBUG:demo_logger:Good status','ERROR:demo_logger:Unknown status: Bad'], lc.output)

    def test_init_logging_debug(self):
        """ Test init logging with level debug"""
        with self.assertLogs(NAME, level='DEBUG') as lc:
            self.form = excel2json("tests/test.xls")
            self.assertEqual([f"INFO:{NAME}:Pass in excel2json.init()"],lc.output)

    def test_worksheet_name(self):
        """ Test the worksheet name """
        self.form = excel2json("tests/test.xls")
        self.assertEqual(['Sheet'], self.form.worksheets)

if __name__ == '__main__':
    unittest.main()