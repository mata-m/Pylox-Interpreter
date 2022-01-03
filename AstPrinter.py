import Expr
import Scanner
import Token
import TokenType

class AstPrinter:
    def printast(self, expr):
        return expr.accept(self)
    
    def parenthesize(self, name, *exprs):
        string = "(" + name
        for expr in exprs:
            string += " "
            # pass the printer to the next subexpr so it can print itself and then return 
            string += expr.accept(self)
        string += ")"
        return string

    def visitBinaryExpr(self, expr):
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visitGroupingExpr(self, expr):
        return self.parenthesize("group", expr.expression)
    
    def visitLiteralExpr(self, expr):
        if expr.value == None:
            return "nil"
        return str(expr.value)
    
    def visitUnaryExpr(self, expr):
        return self.parenthesize(expr.operator.lexeme, expr.right)
    
if __name__ == "__main__":
    expression = Expr.Binary(
        Expr.Unary(
            Token.Token(TokenType.MINUS, "-", None, 1),
            Expr.Literal(123)
        ),
        Token.Token(TokenType.STAR, "*", None, 1),
        Expr.Grouping(Expr.Literal(45.67))
    )

    print(AstPrinter().printast(expression))

