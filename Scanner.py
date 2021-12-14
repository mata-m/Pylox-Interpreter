import TokenType as TType
import Token as tok
import Lox 

class Scanner:
    def __init__(self, source: str):
        self.source  = source
        self.tokens  = [] 
        self.start   = 0 # points to the first char in the lexeme being considered
        self.current = 0 # points to the char being currently considered
        self.line    = 1 # tracks which source line current is on so we produce
                         # tokens that know their line location
        self.keywords = {
            "and":    TType.AND,
            "class":  TType.CLASS,
            "else":   TType.ELSE,
            "false":  TType.FALSE,
            "for":    TType.FOR,
            "fun":    TType.FUN,
            "if":     TType.IF,
            "nil":    TType.NIL,
            "or":     TType.OR,
            "print":  TType.PRINT,
            "return": TType.RETURN,
            "super":  TType.SUPER,
            "this":   TType.THIS,
            "true":   TType.TRUE,
            "var":    TType.VAR,
            "while":  TType.WHILE
        }

    def scanTokens(self):
        while (not self.isAtEnd()):
            # we are at the beginning of the next lexeme
            self.start = self.current
            self.scanToken()
        
        self.tokens.append(tok.Token(TType.EOF, "", None, self.line))
        return self.tokens
    
    def advance(self):
        prevCurrent = self.current
        # Consume the character
        self.current += 1

        return self.source[prevCurrent]

    def addToken(self, type, literal=None):
        # Grabbing the text of the current lexeme
        text = self.source[self.start: self.current]
        # Creating a new token from it and saving it
        self.tokens.append(tok.Token(type, text, literal, self.line))

    
    def match(self, expectedChar):
        if self.isAtEnd():
            return False
        if self.source[self.current] != expectedChar:
            return False
        # Consuming the character since we know it's what we're looking for
        self.current += 1
        return True
        
    def peek(self):
        if self.isAtEnd():
            return '\0'
        return self.source[self.current]
        
    def string(self):
        # Keep advancing the current
        # Keep in mind we still have the start of the lexeme saved
        while self.peek() != '"' and not self.isAtEnd:
            if self.peek() == '\n':
                self.line += 1
            self.advance

        if self.isAtEnd:
            Lox.Lox.error(self.line, "Unterminated string.")
            return
        
        # skip over closing "
        self.advance()

        # slice the string and make a token with it's text as the literal
        # excluding the ""'s
        value = self.source[self.start +1, self.current - 1]
        self.addToken(TType.STRING, value)

    def peekNext(self):
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]

    def number(self):
        # Keep consuming digits
        while self.peek().isdigit():
            self.advance()
        
        # Look for fractional part
        if self.peek() == '.' and self.peekNext().isdigit():
            # consume the '.' since we know there are digits after
            self.advance()
            # consume the rest of the fractional part
            while self.peek().isdigit():
                self.advance()
        
        # finally start is at the beginning of the number
        # and current is at the end of it
        # so add a token for it and pass it the literal this time
        self.addToken(TType.NUMBER, float(self.source[self.start: self.current]))

    def isAlpha(self, c):
        return c.isalpha() or c == '_'

    def identifier(self):
        while self.peek().isalnum():
            self.advance()
        text = self.source[self.start: self.current]
        # Check if identifier is actually a reserved word
        identifierType = TType.IDENTIFIER
        if text in self.keywords:
            identifierType = self.keywords[text]
        self.addToken(identifierType)

    def scanToken(self):
        ch = self.advance()
        print(ch)
        match ch:
            case '(':
                self.addToken(TType.LEFT_PAREN)
            case ')':
                self.addToken(TType.RIGHT_PAREN)
            case '{':
                self.addToken(TType.LEFT_BRACE)
            case '}':
                self.addToken(TType.RIGHT_BRACE)
            case ',':
                self.addToken(TType.COMMA)
            case '.':
                self.addToken(TType.DOT)
            case '-':
                self.addToken(TType.MINUS)
            case '+':
                self.addToken(TType.PLUS)
            case ';':
                self.addToken(TType.SEMICOLON)
            case '*':
                self.addToken(TType.STAR)
            case '!':
                self.addToken(TType.BANG_EQUAL    if self.match("=") else TType.BANG)
            case '=':
                self.addToken(TType.EQUAL_EQUAL   if self.match("=") else TType.EQUAL)
            case '<':
                self.addToken(TType.LESS_EQUAL    if self.match("=") else TType.LESS)
            case '>':
                self.addToken(TType.GREATER_EQUAL if self.match("=") else TType.GREATER)
            case '/':
                if self.match('/'):
                    # Skip the rest of the line as its a comment
                    while not self.isAtEnd() and self.peek() != '\n':
                        self.advance()
                elif self.match('*'):
                    # Keep advancing as long as next to characters aren't end of block comment
                    currentlyOpenStatements = 1
                    while not self.isAtEnd() and currentlyOpenStatements > 0:
                        if self.peek() == '*' and self.peekNext() == '/':
                            currentlyOpenStatements -= 1
                            self.advance()
                            self.advance()
                        elif self.peek() == '/' and self.peekNext() == '*':
                            currentlyOpenStatements += 1
                            self.advance()
                            self.advance()
                        else:
                            if self.peek() == '\n':
                                self.line += 1
                            self.advance()
                else:
                    self.addToken(TType.SLASH)
            case (' ' | '\r' | '\t'):
                pass
            case '\n':
                self.line += 1
            case '"':
                self.string()
            case _:
                if ch.isdigit():
                    self.number()
                elif self.isAlpha(ch):
                    self.identifier()
                else:
                    Lox.Lox.error(self.line, "Unexpected character.")

            

    def isAtEnd(self) -> bool:
        return self.current >= len(self.source)