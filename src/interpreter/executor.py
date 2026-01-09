from node import *
import interpreter.env as env
from interpreter.evaluator import evaluate

from lexer import tokenize
from parser import Parser

# Statement execution and program run separated into executor.
def execute(stmt):
    # Variable assignment
    if isinstance(stmt, Assign):
        env.memory[stmt.name] = evaluate(stmt.value)

    # List assignment: test = [1,2,3]
    elif isinstance(stmt, ListAssign):
        env.memory[stmt.name] = [evaluate(item) for item in stmt.values]

    # List element assignment: test[0] = 10
    elif isinstance(stmt, AssignListElement):
        list_name = stmt.list_access.name
        index = evaluate(stmt.list_access.index)
        value = evaluate(stmt.value)

        if list_name not in env.memory:
            raise Exception(f"Undefined list '{list_name}'")

        env.memory[list_name][index] = value

    # Print
    elif isinstance(stmt, Print):
        print(evaluate(stmt.expr))

    # Input as statement
    elif isinstance(stmt, Input):
        if stmt.prompt:
            return input(stmt.prompt)
        return input()

    # Conditionals
    elif isinstance(stmt, Conditionals):
        if evaluate(stmt.condition):
            for s in stmt.body:
                execute(s)
        elif stmt.elseif_condition is not None and evaluate(stmt.elseif_condition):
            for s in stmt.elseif_body:
                execute(s)
        elif stmt.else_body is not None:
            for s in stmt.else_body:
                execute(s)
    
    # Loops
    elif isinstance(stmt, WhileLoop):
        while evaluate(stmt.condition):
            for s in stmt.body:
                execute(s)
    
    elif isinstance(stmt, ForLoop):
        start = evaluate(stmt.start)
        end = evaluate(stmt.end)

        for i in range(start, end):
            env.memory[stmt.var] = i
            for s in stmt.body:
                execute(s)
                
    # Function definition
    elif isinstance(stmt, Functions):
        env.functions[stmt.name] = stmt

    # Function call
    elif isinstance(stmt, FunctionCall):
        # First check local functions
        if stmt.name in env.functions:
            func = env.functions[stmt.name]

        else:
            # Look in imported modules
            found = False
            for module in env.modules.values():
                if stmt.name in module and isinstance(module[stmt.name], Functions):
                    func = module[stmt.name]
                    found = True
                    break
            if not found:
                # Maybe built-in
                return evaluate(stmt)

        # Check argument count
        if len(stmt.args) != len(func.params):
            raise Exception(
                f"Function '{stmt.name}' expects {len(func.params)} arguments but got {len(stmt.args)}"
            )

        # Evaluate arguments
        arg_values = [evaluate(arg) for arg in stmt.args]

        # Create local memory for function
        old_memory = env.memory
        env.memory = {**env.memory, **dict(zip(func.params, arg_values))}

        # Execute function body statements
        for s in func.body:
            execute(s)

        # Restore previous memory
        env.memory = old_memory


    # expression statements
    elif isinstance(stmt, (ListAccessPos, BinOp, Variable, Number, String)):
        evaluate(stmt)

        # executor.py
    
    elif isinstance(stmt, ImportStatement):
        import_path = stmt.path
        module_name = stmt.alias or import_path.split(".")[0]

        # Read the file
        with open(import_path, "r", encoding="utf-8") as f:
            code = f.read()

        # Tokenize and parse
        tokens = tokenize(code)
        parser = Parser(tokens)
        ast = parser.parse()

        # Create a module dictionary
        module_content = {}

        for node in ast:
            if isinstance(node, Assign):
                module_content[node.name] = evaluate(node.value)
            elif isinstance(node, Functions):
                # store the function AST node
                module_content[node.name] = node

        # Store the module in env.modules
        env.modules[module_name] = module_content
    
    else:
        raise Exception(f"Unknown statement type: {stmt}")


def run(ast):
    for stmt in ast:
        execute(stmt)
