from xlrd import open_workbook, XLRDError
from collections import OrderedDict
import json
import os
import logging
from version import NAME

class excel2json:
    """ This class convert Mooring instrument in Excel file to JSON dictionary """

    def __init__(self, abspath):
        """ :param abspath: absolute path string to excel file """
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
        ''' overload print()'''
        return json.dumps(self._hash, sort_keys=False, indent=4)

    def __getitem__(self, key):
        ''' overloading operators lib[key]'''
        if key not in self._hash:
            self.__logger.error(f"Error! excel2json.__getitem__.py: invalid key: \"{key}\"")
        else:
            return self._hash[key]

    @property
    def worksheets(self):
        ''' worksheets getter
        : return worksheet names as a list'''
        return self._worksheets

    @property
    def hash(self):
        ''' dictonary getter
        : return object as a JSON dictonary'''
        return self._hash

    def __get_excel_sheets(self):
        """ Get details of sheets found in the workbook. """
        try:
            workbook = open_workbook(self.__abspath)
            self._worksheets = workbook.sheet_names()
        except Exception as e:
            self.__logger.error(f"{e}, unable to open worksheet file")

    def __read_excel_sheet(self, sheet_name):
        """ Read the excel sheet and return it.
        :param sheet_name: target excel sheet name string
        :return: worksheet object """
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
        r"""
        Read an excel sheet.
        :param worksheet: worksheet object
        :return: a dictionnary
        """
        ws_dict = OrderedDict({})
        row_dict = OrderedDict({})

        if worksheet is None:
            self.__logger.info("Empty worksheet found.")
            return 1

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
        ''' return python dictionary from JSON string'''
        return OrderedDict(json.loads(self.__str__(), object_pairs_hook=OrderedDict))

    def read(self):
        """ Read an Excel file
        : return a dictionnary"""
        self.__get_excel_sheets()
        for sheet in self._worksheets:
            ws = self.__read_excel_sheet(sheet)
            self._hash[sheet] = self.__worksheet2json(ws)
            #self.__logger.debug(self._hash[sheet])
        return self._hash

    def write(self, filename, path):
        """ :param loc: directory path string (to save files) """
        # dump list of dict to JSON file
        try:
            json_file = os.path.join(path, filename + '.json')
            with open(json_file, 'w') as json_fd:
                # beautify JSON with indentation
                json.dump(
                    self._hash, json_fd, sort_keys=False, indent=4)
            return 0
        except FileNotFoundError as ex:
            self.__logger.error(f'Something wrong with the path "{path}". Error: {ex}.')
            return 1
        except IOError as ex:
            self.__logger.error(
                f'Something wrong happened while saving the file "{filename}.json". Error: {ex}.'
            )
            return 1


if __name__ == '__main__':
    # print(excel2json.convert('test.xlsx'))
    filename = 'library/test.xls'
    lib = excel2json(filename)
    sheet_names = lib.worksheets
    print(sheet_names, end='\n\n')
    # print(lib)
    # print(lib['Anchors'][1], end='\n\n')
    lib.write('test', 'library')
    # fd = open('library/test.json', 'r')
    # h = json.load(fd)
    #h = json.loads(lib.__str__())
    h = lib.toDict()
    print(h['Releases'], end='\n\n')
    print(h['Anchors']['1'], end='\n\n')
    print(h['Ropes']['1'].keys(), end='\n\n')
