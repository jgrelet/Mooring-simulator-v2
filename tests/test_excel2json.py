"""Collection of tests around log handling."""

import unittest
import shutil
import tempfile
from os import path

from logger import configure_logger
from excel2json import excel2json
from version import NAME

class testExcel2json(unittest.TestCase):

    def setUp(self):

        # test.xls dump dict
        self.hash = {
            "1": {
                "Column1": "row1"
            },
            "2": {
                "Column1": "row2"
            }
        }
        self.dump = '''{
    "Sheet": {
        "1": {
            "Column1": "row1"
        },
        "2": {
            "Column1": "row2"
        }
    }
}'''

        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Remove the directory after the test
        shutil.rmtree(self.test_dir)

    # def test_init_logging_info(self):
    #     """ Test init logging with level info"""
    #     with self.assertLogs(NAME, level='INFO') as lc:
    #         self.form = excel2json("library/example.xls")
    #         self.assertEqual([], lc.output)

    def test_init_logging_debug(self):
        """ Test init logging with level debug"""
        with self.assertLogs(NAME, level='DEBUG') as lc:
            self.form = excel2json("tests/test.xls")
            self.assertEqual(
                [f"DEBUG:{NAME}:Pass in excel2json.init()"], lc.output)

    def test_worksheet_name(self):
        """ Test the worksheet name = sheet """
        self.form = excel2json("tests/test.xls")
        self.assertEqual(['Sheet'], self.form.worksheets)

    def test_worksheet_values(self):
        """ Test default values in Excel test.xls"""
        self.form = excel2json("tests/test.xls")
        h = self.form.toDict()
        d = h['Sheet']
        for k in d.keys():
            self.assertEqual(d[k], self.hash[k])

    def test_write_json(self):
        """ Test write to json tmp file """
        self.form = excel2json("tests/test.xls")
        file = self.form.write('test', self.test_dir)
        fd = open(path.join(self.test_dir, 'test.json'), 'r')
        self.assertEqual(fd.read(), self.dump)
        fd.close()

    # add write test.json, remove file, add and delete values


if __name__ == '__main__':
    unittest.main()
