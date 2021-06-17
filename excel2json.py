from xlrd import open_workbook, XLRDError
from collections import OrderedDict
import json
import os
import logging
from version import NAME


class excel2json:
    """This class convert Mooring instrument in Workbook Excel
     file to an ordered JSON dictionary """

    def __init__(self, abspath):
        """excel2json constructor from Workbook Excel file name.

        Args:
            abspath (str): absolute path string to Workbook Excel file
        """
        # protected properties with decorators
        self._worksheets = []
        self._hash = OrderedDict({})
        # private properties
        self.__logger = logging.getLogger(NAME)
        self.__logger.debug("Pass in excel2json.init()")
        self.__abspath = abspath
        # call methods
        self.read()

    def __str__(self):
        """Overload print() method

        Returns:
            str: a JSON dump of the Workbook
        """
        return json.dumps(self._hash, sort_keys=False, indent=4)

    def __getitem__(self, key):
        ''' overloading operators lib[key]'''
        if key not in self._hash:
            self.__logger.error(
                f"excel2json.__getitem__.py: invalid key: \"{key}\"")
        else:
            return self._hash[key]

    @property
    def worksheets(self):
        """Getter to protected worksheets property 

        Returns:
            list: the list of sheets found in the Workbook
        """
        return self._worksheets

    @property
    def hash(self):
        """Getter to protected hash dictionary property
       
        Returns:
            OrderedDict: an object as a JSON dictonary
        """
        return self._hash

    def __get_sheet_names(self):
        """Get the list of sheets found in the Workbook.
        """
        try:
            workbook = open_workbook(self.__abspath)
            self._worksheets = workbook.sheet_names()
        except Exception as e:
            self.__logger.error(f"{e}, unable to open worksheet file")

    def __read_sheet(self, sheet_name):
        """Read the Workbook sheet and return it.

        Args:
            sheet_name (str): target Workbook sheet name string
            to be opened

        Returns:
            Book: An instance of the ~xlrd.book.Book class.
        """
        # python module 'xlrd' supports .xls & .xlsx both
        try:
            workbook = open_workbook(self.__abspath)
            # return the specified worksheet
            return workbook.sheet_by_name(sheet_name)
        except FileNotFoundError as ex:
            self.__logger.error(
                f"Something wrong with the path {self.__abspath}. Error: {ex}.")
            return None
        except XLRDError as ex:
            self.__logger.error(
                f"Something wrong happened while reading the Excel file. Error: {ex}"
            )
            return None
        except Exception as ex:
            self.__logger.error(
                f"Something wrong happened while reading the Excel file. Error: {ex}"
            )
            return None

    def __worksheet2json(self, worksheet):
        """Read an Workbook worksheet as a ordered dictionary

        Args:
            worksheet (str): worksheet name

        Returns:
            OrderedDict: an ordered dictionary containing the data
        """
        ws_dict = OrderedDict({})
        row_dict = OrderedDict({})

        if worksheet is None:
            self.__logger.info("Empty worksheet found.")
            return None

        # store row 1 (column headers)
        header = [cell.value for cell in worksheet.row(0)]
        key = 0

        # read each row except header, create dict per row and append to the list
        for row in range(1, worksheet.nrows):
            row_dict = {value: worksheet.cell(
                row, col).value for col, value in enumerate(header)}
            ws_dict[str(row)] = row_dict
            row_dict = {}
        return ws_dict

    def toDict(self):
        """Return python ordered dictionary from JSON string

        Returns:
            OrderedDict: a JSON string representing the worksheet data
        """
        return OrderedDict(json.loads(self.__str__(), object_pairs_hook=OrderedDict))

    def read(self):
        """Read an Workbook (Excel) file, store each worksheet
        in a hash

        Returns:
            OrderedDict: an ordered dictionary containing the data
        """
        self.__get_sheet_names()
        for sheet in self._worksheets:
            ws = self.__read_sheet(sheet)
            self._hash[sheet] = self.__worksheet2json(ws)
            # self.__logger.debug(self._hash[sheet])
        return self._hash

    def write(self, filename, path):
        """Write the Workbook as a JSON file

        Args:
            filename (str): JSON file name
            path (str):  path 

        Returns:
            str: the full path name, none in case of failure 
        """
        # dump list of dict to JSON file
        try:
            json_file = os.path.join(path, filename + '.json')
            with open(json_file, 'w') as json_fd:
                # beautify JSON with indentation
                json.dump(
                    self._hash, json_fd, sort_keys=False, indent=4)
            return json_file
        except FileNotFoundError as ex:
            self.__logger.error(
                f'Something wrong with the path "{path}". Error: {ex}.')
            return None
        except IOError as ex:
            self.__logger.error(
                f'Something wrong happened while saving the file "{filename}.json". Error: {ex}.'
            )
            return None


if __name__ == '__main__':

    from logger import configure_logger
    logger = configure_logger('INFO')
    logger = logging.getLogger(NAME)
    logger.info("Logging OK.")

    # lib = excel2json('library/example.xls')
    # sheet_names = lib.worksheets
    # print(sheet_names, end='\n\n')
    # # print(lib)
    # # print(lib['Anchors'][1], end='\n\n')
    # lib.write('test', 'library')
    # # fd = open('library/test.json', 'r')
    # # h = json.load(fd)
    # #h = json.loads(lib.__str__())
    # h = lib.toDict()
    # print(h['Releases'], end='\n\n')
    # print(h['Anchors']['1'], end='\n\n')
    # print(h['Ropes']['1'].keys(), end='\n\n')

    lib = excel2json('tests/test.xls')
    sheet_names = lib.worksheets
    print(sheet_names, end='\n\n')
    lib.write('test', 'tests')
    print(lib['Sheet']['1'])
    print(lib['Sheet']['2'])
    print(lib['dummy'])
    h = lib.toDict()
    print(h['Sheet'], end='\n\n')
    print(h['Sheet']['1'], end='\n\n')
    print(h['Sheet']['2'], end='\n\n')
    #print(h['Sheet']['3'], end='\n\n')
    # print(h['dummy']['1'], end='\n\n')
