import ast
import operator as op

# supported operators
operators = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.BitXor: op.xor,
    ast.USub: op.neg,
}


def EvalMathExpr(expr):
    if expr:
        try:
            return _eval_(ast.parse(expr, mode="eval").body)
        except:
            pass


def _eval_(node):
    if isinstance(node, ast.Num):  # <number>
        return node.n
    elif isinstance(node, ast.BinOp):  # <left> <operator> <right>
        return operators[type(node.op)](_eval_(node.left), _eval_(node.right))
    elif isinstance(node, ast.UnaryOp):  # <operator> <operand> e.g., -1
        return operators[type(node.op)](_eval_(node.operand))
    else:
        raise TypeError(node)


def CastToNumberIfPossible(string):
    try:
        return float(string)
    except:
        return False
