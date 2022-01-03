import Token

class Expr:
    pass

class Visitor:
    def visitUnaryExpr(unaryExpr):
        pass
    def visitBinaryExpr(binaryExpr):
        pass
    def visitGroupingExpr(groupingExpr):
        pass
    def visitLiteralExpr(literalExpr):
        pass

class Unary(Expr):
    def __init__(self, operator, right):
        assert isinstance(operator, Token.Token)
        assert isinstance(right, Expr)

        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visitUnaryExpr(self)

class Binary(Expr):
    def __init__(self, left, operator, right):
        assert isinstance(left, Expr)
        assert isinstance(operator, Token.Token)
        assert isinstance(right, Expr)

        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visitBinaryExpr(self)

class Grouping(Expr):
    def __init__(self, expression):
        assert isinstance(expression, Expr)

        self.expression = expression

    def accept(self, visitor):
        return visitor.visitGroupingExpr(self)

class Literal(Expr):
    def __init__(self, value):
        assert isinstance(value, object)

        self.value = value

    def accept(self, visitor):
        return visitor.visitLiteralExpr(self)
