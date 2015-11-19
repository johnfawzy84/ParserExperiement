from pyparsing import Word, delimitedList, Optional, \
    Group, alphas, nums, alphanums, Forward, quotedString, \
    ZeroOrMore


class TokensGenerator():
    def __init__(self):
        self.primitive_cmd = None
        self.parse_primitive()
        self.macro_call_cmd = None
        self.parse_macro_call()
        self.full_macro = None
        self.parse_full_macro()

    def parse_primitive(self):
        castlestmt = Forward()
        hex_str = quotedString
        lid = Word(alphas, alphanums + "_").setResultsName("localid")
        sid = Word(alphas, alphanums + "_").setResultsName("serviceid")
        parameter = Word(alphas, alphanums + "_").setResultsName("parameter")
        #
        value = (Word(alphanums + "&", alphanums + "_") | hex_str).setResultsName("value")
        param_val = (parameter + value).setResultsName("param_val")
        param_val_grp = ZeroOrMore(param_val).setResultsName("param_val_grp")
        time_stamp = Word(nums, nums).setResultsName("timestamp")
        castlestmt << time_stamp + lid + ":" + sid + Optional("{" + param_val_grp + "}")
        self.primitive_cmd = castlestmt

    def parse_macro_call(self):
        macrocallstmt = Forward()
        time_stamp = Word(nums, nums).setResultsName("timestamp")
        macro_func = Word(alphas, alphanums + "_").setResultsName("macro_func")

        hex_str = quotedString
        parameter = Word(alphas, alphanums + "_").setResultsName("parameter")
        value = (Word(alphanums + "&", alphanums + "_") | hex_str).setResultsName("value")
        param_val = (parameter + value).setResultsName("param_val")
        param_val_grp = Group(delimitedList(param_val)).setResultsName("param_val_grp")

        macrocallstmt << time_stamp + macro_func + "(" + Optional(param_val_grp) + ")"
        self.macro_call_cmd = macrocallstmt

    def parse_full_macro(self):
        fullmacro = Forward()
        macro_name = Word(alphas, alphanums + "_").setResultsName("macro_name")
        macrocallline = Group((self.macro_call_cmd | self.primitive_cmd)).setResultsName("line")
        macrocallsline = ZeroOrMore(macrocallline).setResultsName('lines')
        fullmacro << macro_name + '{' + macrocallsline + '}'
        self.full_macro = fullmacro
