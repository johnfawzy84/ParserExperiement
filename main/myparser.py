from pyparsing import ParseException

from main.LibraryClasses import PrimitiveCastleCommand, CastleMacroCall, CastleFullMacro, FullMacroLine, \
    CommandParam
from main.TokensGenerator import TokensGenerator

y = None


class CastleLibraryFileParser():


    def test_primitive(self,str):
        cstle_cmd = PrimitiveCastleCommand()
        cmd_parsr = TokensGenerator()
        print str, "->"
        try:
            tokens = cmd_parsr.primitive_cmd.parseString(str)
            print "tokens = ", tokens
            print "tokens.localid =", tokens.localid
            cstle_cmd.LID = tokens.localid
            print "tokens.serviceid =", tokens.serviceid
            cstle_cmd.SID = tokens.serviceid
            for i in range(0, len(tokens.param_val_grp), 2):
                cstle_cmd.parameters.append((tokens.param_val_grp[i], tokens.param_val_grp[i + 1]))
            print "tokens.params =", cstle_cmd.parameters
            print
            # print "tokens.where =", tokens.where
            return (cstle_cmd, tokens)
        except ParseException, err:
            print " " * err.loc + "^\n" + err.msg
            print err
            return None


    def test_macro_call(self,str):
        cstle_macro = CastleMacroCall()
        cmd_parsr = TokensGenerator()
        print str, "->"
        try:
            tokens = cmd_parsr.macro_call_cmd.parseString(str)
            print "tokens = ", tokens
            print "tokens.fnc_name =", tokens.macro_func
            cstle_macro.fnc_name = tokens.macro_func
            for i in range(0, len(tokens.param_val_grp), 2):
                cstle_macro.parameters.append((tokens.param_val_grp[i], tokens.param_val_grp[i + 1]))
            print "tokens.params =", cstle_macro.parameters
            print
            return (cstle_macro, tokens)
            # print "tokens.where =", tokens.where
        except ParseException, err:
            print " " * err.loc + "^\n" + err.msg
            print err
            return None


    def test_full_macro(self,str):
        global y
        cstle_fmacro = CastleFullMacro()
        cmd_parsr = TokensGenerator()
        print str, "->"
        try:
            tokens = cmd_parsr.full_macro.parseString(str)
            print "tokens = ", tokens
            print "tokens.fnc_name =", tokens.macro_name
            cstle_fmacro.macro_name = tokens.macro_name
            print "tokens.lines =", tokens.lines
            # cstle_fmacro.lines.append(tokens.lines)
            for myline in tokens.lines:
                if ":" in list(myline):
                    # primitive line
                    primtive_line = PrimitiveCastleCommand()
                    fmacro_line = FullMacroLine()
                    fmacro_line.isMacroCall = False
                    fmacro_line.isPrimitive = True
                    fmacro_line.time_stamp = myline.timestamp
                    primtive_line.LID = myline.localid
                    primtive_line.SID = myline.serviceid
                    param_val_list = list(myline.param_val_grp)
                    for att_i in range(0, len(myline.param_val_grp), 2):
                        new_param = CommandParam()
                        new_param.param_name = param_val_list[att_i]
                        new_param.param_val = param_val_list[att_i + 1]
                        primtive_line.parameters.append(new_param)
                    # fmacro_line.line = PrimitiveCastleCommand()
                    fmacro_line.line = primtive_line
                    cstle_fmacro.lines.append(fmacro_line)
                elif "(" in list(myline):
                    # macro call
                    macro_call_line = CastleMacroCall()
                    fmacro_line = FullMacroLine()
                    fmacro_line.isMacroCall = True
                    fmacro_line.isPrimitive = False
                    fmacro_line.time_stamp = myline.timestamp
                    macro_call_line.fnc_name = myline.macro_func
                    param_list = list(myline.param_val_grp)
                    for i in range(0, len(param_list), 2):
                        new_param = CommandParam()
                        new_param.param_name = param_list[i]
                        new_param.param_val = param_list[i + 1]
                        macro_call_line.parameters.append(new_param)
                    fmacro_line.line = macro_call_line
                    cstle_fmacro.lines.append(fmacro_line)
            return (cstle_fmacro, tokens, cmd_parsr)
        except ParseException, err:
            print " " * err.loc + "^\n" + err.msg
            print err
            return None


# \n ww 33 \n xxx &d1}"
# test("Klemme15:On{ xy  99 99 99 }" )
# test("10\tKlemme15:On{ \n xy  \"99 99 99\" \n }"  )
# test("100\tKlemme15:On{ \n ww 33\n }" )
# test("200\tKlemme15:On{ \n xxx &d1 \n }" )
# test("10010\tKlemme15:On{ \n ww 33 \n xxx &d1 \n}" )
# test("500\tMFrTxXXX:Send")
# test("1\tDiag:Send")
# test("12487\tx::send")
# test_macro("100\tmacro333(b1 999,b2 &b1)")
# test("100\tmacro333(b1 999,b2 &b1)")
# test_macro("0\t\tCalculate_Access_Key(b1 0x02, b2 0x07, b3 0x40, b4 0x02)")
# test_macro("5\t\tDiag_Modify(b1 0x00, b2 0x07, b3 0x08, d1 \"27\")")
# test_macro("10\t\tDiag_Modify(b1 0x01, b2 0x07, b3 0x08,d1 &d1)")
# test_macro("15\t\tDiag_Push_Functional()")
'''
THIS IS  A NEW COMMENT TO TRY COMMITTING --- TODAY 19.11.2015
'''
macro = "Send_Invalid_Security_Key_Functional\n{\n0\t\tCalculate_Access_Key(b1 0x02, b2 0x07, b3 0x40, b4 0x02)"
macro += "\n5\t\tDiag_Modify(b1 0x00, b2 0x07, b3 0x08, d1 \"27\")\n10\t\tDiag_Modify(b1 0x01, b2 0x07, b3 0x08,"
macro += "d1 &d1)\n15\t\tDiag_Push_Functional()\n}"

macro2 = "Send_Invalid_Security_Key_Functional\n{\n0\t\tCalculate_Access_Key(b1 0x02, b2 0x07, b3 0x40, b4 0x02)\n}"

macro3 = "Send_Invalid_Security_Key_Functional\n{\n0\t\tCalculate_Access_Key:xxx{\nb1 0x02\nb2 0x07\nb3 0x40\nb4 0x02\n}\n10\t\tCalculate_Access_Key:xxx{\nb1 0x02\nb2 0x07\nb3 0x40\nb4 0x02\n}}"
macro4 = "Send_Invalid_Security_Key_Functional\n{\n0\t\tCalculate_Access_Key:xxx{\nb1 0x02\nb2 0x07\nb3 0x40\nb4 0x02\n}\n10\t\tCalculate_Access_Key2:yy{\nb1 &b44\nb2 0x07\nb3 0x40\nb4 0x02\n}\n100\tmacro333(b1 999,b2 &b1)}"
x = CastleLibraryFileParser()
y = x.test_full_macro(macro + macro2 + macro3 + macro4)
print "Finished!!"
