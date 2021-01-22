from src.Core.Log import Log


def ASSERT(condition, msg=""):
    if not condition:
        Log.Error(msg)
        raise Exception(msg)
