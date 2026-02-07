from node import *
import interpreter.env as env

from runtime.builtins import builtins, BuiltinFunction
from error import InterpreterError

# Expression evaluation separated into its own module.
def evaluate(node):
    if isinstance(node, Number):
        return node.value

    elif isinstance(node, String):
        return node.value

    elif isinstance(node, Variable):
        if node.name in env.memory:     
            return env.memory[node.name]
        
        if node.name in builtins:
            return builtins[node.name]
        raise InterpreterError(f"ያልታወቀ መለያ ስም -> '{node.name}'")
        
    elif isinstance(node, ListAssign) and node.name is None:
        return [evaluate(item) for item in node.values]

    elif isinstance(node, ListAccessPos):
        if node.name not in env.memory:
            raise InterpreterError(f"ያልታወቀ የዝርዝር መለያ ስም '{node.name}'")
        lst = env.memory[node.name]
        index = evaluate(node.index)
        return lst[index]

    elif isinstance(node, BinOp):
        left = evaluate(node.left)
        right = evaluate(node.right)

        if node.op == '+':
            return left + right
        elif node.op == '-':
            return left - right
        elif node.op == '*':
            return left * right
        elif node.op == '/':
            return left / right

        elif node.op == '>':
            return left > right
        elif node.op == '<':
            return left < right
        elif node.op == '>=':
            return left >= right
        elif node.op == '<=':
            return left <= right
        elif node.op == '==':
            return left == right
        elif node.op == '!=':
            return left != right

        elif node.op == '&&':
            return left and right
        elif node.op == '||':
            return left or right

        else:
            raise InterpreterError(f"ያልታወቀ ምልክት -> '{node.op}'")

    elif isinstance(node, Input):
        if node.prompt:
            return input(node.prompt)
        return input()
    
    elif isinstance(node, FunctionCall):
        # Resolve function reference. `node.name` may be a ModuleAccess node
        # (for module/class member calls) or a plain identifier.
        if isinstance(node.name, ModuleAccess):
            func = evaluate(node.name)
        else:
            func = evaluate(Variable(node.name))

        args = [evaluate(arg) for arg in node.args]

        # Builtin functions
        if hasattr(func, "call"):
            return func.call(args)

        # User-defined function AST (Functions)
        if isinstance(func, Functions):
            if len(args) != len(func.params):
                raise InterpreterError(
                    f"ተግባር '{func.name}' {len(func.params)} ፓራሜተሮችን ጠብቆ ነበር ግን {len(args)} አገኘ።"
                )

            # execute function body in local memory
            old_memory = env.memory
            env.memory = {**env.memory, **dict(zip(func.params, args))}
            # import execute here to avoid circular imports at module import time
            from interpreter.executor import execute
            for s in func.body:
                execute(s)
            env.memory = old_memory
            return None

        raise InterpreterError(f"'{getattr(node.name, 'name', node.name)}' እንደ ተግባር ተጠሪ አይደለም።")

    elif isinstance(node, ClassCall):
        classname = evaluate(Variable(node.name))
        functions = [evaluate(function) for function in node.functionName]

        if hasattr(classname, "call"):
            return classname.call(functions)

    elif isinstance(node, ModuleAccess):
        # First check builtin modules (e.g. `math`) registered in runtime.builtins
        if node.module_name in builtins and isinstance(builtins[node.module_name], dict):
            module = builtins[node.module_name]
            if node.member_name not in module:
                raise InterpreterError(f"Module '{node.module_name}' -> '{node.member_name}' ሚባል አባል የለውም።")
            return module[node.member_name]

        # Then check imported modules
        if node.module_name in env.modules:
            module = env.modules[node.module_name]
            if node.member_name not in module:
                raise InterpreterError(f"Module '{node.module_name}' -> '{node.member_name}' ሚባል አባል የለውም።")
            return module[node.member_name]

        # Then check locally defined classes
        if node.module_name in env.classes:
            classname = env.classes[node.module_name]
            for s in classname.body:
                if isinstance(s, Functions) and s.name == node.member_name:
                    return s
            raise InterpreterError(f"ክፍል '{node.module_name}' -> '{node.member_name}' ሚባል አባል የለውም።")

        raise InterpreterError(f"Module ወይም ክፍል '{node.module_name}' የሚባል የለም")  # Functions node or variable


    
    else:
        raise InterpreterError(f"Cannot evaluate node: {node}")
