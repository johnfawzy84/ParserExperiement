from os import path


class lib_files_handler():
    '''
    This is a class responsible of handling the CASTLE libraries
    '''
    def __init__(self):
        # self.file_list = []
        self.files_txt = ""
        self.main_lib_file_path = ""
        self.extracted_low_level_functions = ""

    def add_lib_txt(self, include_line):
        # library path
        libp = include_line[include_line.find("\\"):include_line.rfind("\"")]
        # full library path
        flibp = path.join(self.main_lib_file_path, libp)
        # library file
        libf = open(flibp)
        for line in libf:
            self.files_txt = self.files_txt + line

    def find_and_parse_macro(self, func_name):
        '''
        The function aim to get the low level functions for a macro
        :param func_name: macro name
        :return: timed low level functions
        '''

    def get_lib_files_and_gen_txt(self, fpath):
        self.main_lib_file_path = fpath[:fpath.rfind("\\")]
        main_lib_f = open(fpath, 'r')
        for line in main_lib_f:
            if "@INCLUDE" in line:
                self.add_lib_txt(line)
