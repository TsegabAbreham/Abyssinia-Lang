from node import *
import interpreter.env as env

from runtime.builtins import builtins, BuiltinFunction

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
        raise Exception(f"Undefined variable '{node.name}'")
        
    elif isinstance(node, ListAssign) and node.name is None:
        return [evaluate(item) for item in node.values]

    elif isinstance(node, ListAccessPos):
        if node.name not in env.memory:
            raise Exception(f"Undefined list '{node.name}'")
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
            raise Exception(f"Unknown operator '{node.op}'")

    elif isinstance(node, Input):
        if node.prompt:
            return input(node.prompt)
        return input()
    
    elif isinstance(node, FunctionCall):
        func = evaluate(Variable(node.name))
        args = [evaluate(arg) for arg in node.args]

        if hasattr(func, "call"):
            return func.call(args)

        raise Exception(f"'{node.name}' is not callable")

    elif isinstance(node, ModuleAccess):
        if node.module_name not in env.modules:
            raise Exception(f"Module '{node.module_name}' is not imported")
        
        module = env.modules[node.module_name]

        if node.member_name not in module:
            raise Exception(f"Module '{node.module_name}' has no member '{node.member_name}'")
        
        return module[node.member_name]  # Functions node or variable




    else:
        raise Exception(f"Cannot evaluate node: {node}")
