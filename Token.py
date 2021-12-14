class Token:
    def __init__(self, type, lexeme, literal, line):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line
    
    def toString(self) -> str:
        return f"{str(self.type)[10:]} {self.line} {self.lexeme} {self.literal}"