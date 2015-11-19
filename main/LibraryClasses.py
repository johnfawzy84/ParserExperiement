class CommandParam():
    def __init__(self):
        self.param_name = ""
        self.param_val = ""


class PrimitiveCastleCommand():
    def __init__(self):
        self.LID = ""
        self.SID = ""
        self.parameters = []


class CastleMacroCall():
    def __init__(self):
        self.fnc_name = ""
        self.parameters = []


class FullMacroLine():
    def __init__(self):
        self.time_stamp = ""
        self.isPrimitive = False
        self.isMacroCall = False
        self.line = None


class CastleFullMacro():
    def __init__(self):
        self.macro_name = ""
        self.lines = []
