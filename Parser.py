import Token
import TokenType as TT
import Expr
import Lox

class Parser:
    class ParseError(Exception):
        """Raise for an unexpected token in the parser."""

    def __init__(self, token_list, lox):
        # Parser's read in tokens from the scanner
        self.token_list = token_list
        self._current = 0
        self.lox = lox

    def _synchronize(self):
        self.advance()
        while not self._isAtEnd():
            # Continue discarding tokens until reached end of statement (synced)
            if self.previous().type == TT.SEMICOLON:
                return
            
            match self.peek().type:
                case TT.CLASS:
                    return
                case TT.RETURN:
                    return
                case TT.FOR:
                    return
                case TT.FUN:
                    return
                case TT.IF:
                    return
                case TT.PRINT:
                    return
                case TT.VAR:
                    return
                case TT.WHILE:
                    return
            self.advance()

    def _error(self, token, message):
        # Log the error with the interpreter
        self.lox.error(self.lox, token=token, errorMsg=message)
        # Synchronization is handled through throwing ParseError object to clear out call frames
        return self.ParseError()

    def _peek(self):
        return self.token_list[self._current]

    def _previous(self) -> Token.Token:
        return self.token_list[self._current - 1]

    def _isAtEnd(self):
        return self._peek().type == TT.EOF

    def _advance(self):
        # _consumes token and returns it
        if not self._isAtEnd():
            self._current += 1
        return self._previous()

    def _check(self, type: TT) -> bool:
        if self._isAtEnd():
            return False
        return self._peek().type == type
        

    def _match(self, *types):
        for type in types:
            if self._check(type): # Check if curr type has any of the given types
                self._advance()
                return True
        return False
            

    def _consume(self, tokenType, errorMsg):
        # Consumes the next token if its the given type
        if  self._check(tokenType):
            return self._advance()
        raise self._error(self._peek(), errorMsg)

    def _primary(self):
        if self._match(TT.FALSE):
            return Expr.Literal(False)
        if self._match(TT.TRUE):
            return Expr.Literal(True)
        if self._match(TT.NIL):
            return Expr.Literal(None)
        
        if self._match(TT.NUMBER, TT.STRING):
            return Expr.Literal(self._previous().literal)
        
        if self._match(TT.LEFT_PAREN):
            expr = self._expression()
            self._consume(TT.RIGHT_PAREN, "Expect ')' after expression.")
            return Expr.Grouping(expr)
        # We are sitting on a token that can't start an expression
        raise self._error(self._peek(), "Expect expression.")
    
    def _unary(self):
        if self._match(TT.BANG, TT.SLASH):
            operator = self._previous()
            right = self._unary()
            return Expr._unary(operator, right)

        return self._primary()


    def _factor(self):
        expr = self._unary()

        while self._match(TT.SLASH, TT.STAR):
            operator = self._previous()
            right = self._unary()
            expr = Expr.Binary(expr, operator, right)
        
        return expr

    def _term(self):
        expr = self._factor()

        while self._match(TT.MINUS, TT.PLUS):
            operator = self._previous()
            right = self._factor()
            expr = Expr.Binary(expr, operator, right)

        return expr
        
    
    def _comparison(self) -> Expr.Expr:
        expr = self._term()

        while self._match(TT.GREATER, TT.GREATER_EQUAL, TT.LESS, TT.LESS_EQUAL):
            operator = self._previous()
            right = self._term()
            expr = Expr.Binary(expr, operator, right)

        return expr

    def _equality(self) -> Expr.Expr:
        expr = self._comparison()
        # Keep building the syntax tree by composing binary _comparison _expressions inside of another until done
        while self._match(TT.BANG_EQUAL, TT.EQUAL_EQUAL):
            # _match _advances the tokens so it skipped over the operator
            operator = self._previous()
            right = self._comparison()
            # Combine the operator and both operands into a new Expr.Binary syntax tree node (Composing _previous compar expr into new one)
            # This creates a left-associative nested tree of binary operator nodes
            expr = Expr.Binary(expr, operator, right)
        return expr

    def _comma_block(self) -> Expr.Expr:
        expr = self._equality()

        if self._match(TT.COMMA):
            operator = self._previous() # The comma
            # Go grab the second part of the block statement
            right = self._equality()

            expr = Expr.Binary(expr, operator, right)

        return expr

    def _expression(self):
        return self._comma_block()

    def parse(self):
        try:
            return self._expression()
        except self.ParseError as error:
            return None
