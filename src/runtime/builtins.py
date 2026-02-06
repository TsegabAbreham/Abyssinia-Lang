from error import InterpreterError


class BuiltinFunction:
    def __init__(self, fn, arity=None):
        self.fn = fn
        self.arity = arity

    def call(self, args):
        if self.arity is not None and len(args) != self.arity:
            raise InterpreterError("Wrong number of arguments")
        try:
            return self.fn(*args)
        except InterpreterError:
            raise
        except Exception:
            # Hide internal python errors from the user; surface as interpreter error
            raise InterpreterError("Runtime error in builtin function")


builtins = {
    "ሂሳብ": {},
    "ጽሁፍ": {},
    "ዝርዝር": {},
    "ፋይል": {},
    "ኢንተርኔት": {}
}

# --------  MATH ---------------
import math 
import random

def b_abs(x):
    return abs(x)

def b_round(x, n):
    return round(x, n)

def b_sqrt(x):
    return math.sqrt(x)

def b_pow(x, y):
    return pow(x, y)

def b_max(*n):
    return max(n)

def b_min(*n):
    return min(n)

def b_randint(a, b):
    return random.randint(a, b)

def b_sin(x):
    return math.sin(x)

def b_cos(x):
    return math.cos(x)

def b_tan(x):
    return math.tan(x)

def b_asin(x):
    return math.asin(x)

def b_acos(x):
    return math.acos(x)

def b_atan(x):
    return math.atan(x)


builtins["ሂሳብ"]["abs"]  = BuiltinFunction(b_abs, 1)
builtins["ሂሳብ"]["round"]  = BuiltinFunction(b_round, 2)
builtins["ሂሳብ"]["sqrt"]  = BuiltinFunction(b_sqrt, 1)
builtins["ሂሳብ"]["pow"]  = BuiltinFunction(b_pow, 2)
builtins["ሂሳብ"]["max"]  = BuiltinFunction(b_max)
builtins["ሂሳብ"]["min"]  = BuiltinFunction(b_min)
builtins["ሂሳብ"]["randint"]  = BuiltinFunction(b_randint, 2)
builtins["ሂሳብ"]["sin"]  = BuiltinFunction(b_sin, 1)
builtins["ሂሳብ"]["cos"]  = BuiltinFunction(b_cos, 1)
builtins["ሂሳብ"]["tan"]  = BuiltinFunction(b_tan, 1)
builtins["ሂሳብ"]["asin"]  = BuiltinFunction(b_asin, 1)
builtins["ሂሳብ"]["acos"]  = BuiltinFunction(b_acos, 1)
builtins["ሂሳብ"]["atan"]  = BuiltinFunction(b_atan, 1)

# -------- String -----------


def b_len(value):
    return len(value)

def b_replace(value, old, new):
    return value.replace(old, new)

def b_split(value, separator):
    return value.split(separator)

builtins["ጽሁፍ"]["ርዝመት"] = BuiltinFunction(b_len, 1)
builtins["ጽሁፍ"]["ተካ"] = BuiltinFunction(b_replace, 3)
builtins["ጽሁፍ"]["ክፈል"] = BuiltinFunction(b_split, 2)

# --------- Data type conversion ----------
def b_tostr(value):
    return str(value)
def b_toint(value):
    return int(value)
def b_tofloat(value):
    return float(value)

builtins["ወደጽሁፍ"] = BuiltinFunction(b_tostr, 1)
builtins["ወደቁጥር"] = BuiltinFunction(b_toint, 1)
builtins["ወደነጥብቁጥር"] = BuiltinFunction(b_tofloat, 1)
# --------- List Variables ------------

def b_append(value, var=None):
    if var is None:
        var = []
    var.append(value)
    return var


builtins["ዝርዝር"]["ጨምር"] = BuiltinFunction(b_append, 2)

# -------- FILE I/O BUILTINS --------

def b_open(path, mode):
    return open(path, mode)

def b_write(file_or_path, content):
    content = str(content)
    # If it's already a file object, just write
    if hasattr(file_or_path, "write"):
        file_or_path.write(content)
    # If it's a string path, open it and write
    else:
        with open(file_or_path, "w", encoding="utf-8") as f:
            f.write(content)
    return None

def b_read(file_or_path):
    if hasattr(file_or_path, "read"):
        return file_or_path.read()
    else:
        with open(file_or_path, "r", encoding="utf-8") as f:
            return f.read()

def b_close(file_or_path):
    if hasattr(file_or_path, "close"):
        file_or_path.close()
    return None



builtins["ፋይል"]["ክፈት"]  = BuiltinFunction(b_open, 2)
builtins["ፋይል"]["አንብብ"]  = BuiltinFunction(b_read, 1)
builtins["ፋይል"]["ጻፍ"] = BuiltinFunction(b_write, 2)
builtins["ፋይል"]["ዝጋ"] = BuiltinFunction(b_close, 1)

# --------- REQUESTING ------------
import requests

def b_get(url, mode):
    resp = requests.get(url)

    if mode == "አዎ":  # status + body
        return {
            "status": resp.status_code,
            "body": resp.json()
        }

    elif mode == "ብቻ":  # status only
        return resp.status_code

    else:  # body only
        return resp.text


    
builtins["ኢንተርኔት"]["አግኝ"] = BuiltinFunction(b_get, 2)