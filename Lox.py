import sys
import typing as tp
import AstPrinter as ast
import Scanner as sc
import Parser as prs
import TokenType as TT
# TODO write an ErrorReporter class later to further abstract the error reporting

class Lox:
    def __init__(self, args: tp.Sequence[str]):
        self.hadError = False
        if len(args) > 2:
            print("Usage: pylox [file_path]")
            return 64
        if len(args) == 2:
            self.runFile(args[1])
        else:
            self.runPrompt()

    @staticmethod
    def report(self, line: int, where: str, message: str):
        print("[line " + str(line) + "] Error" + where + ": " + message)
        self.hadError = True

    @staticmethod
    def error(self, line: int, message: str):
        self.report(line, "", message)

    @staticmethod
    def error(self, token, errorMsg):
        #Returns ParseError and logs an error with the interpreter
        if token.type == TT.EOF:
            self.report(self, token.line, "at end", errorMsg)
        else:
            self.report(token.line, " at " + token.lexeme + "'", errorMsg)

    def run(self, source: str):
        print(source)
        scanner = sc.Scanner(source)
        tokens = scanner.scanTokens()
        parser = prs.Parser(tokens, lox=self)
        expression = parser.parse()

        # For now just printing the tokens
        #for token in tokens:
        #    print(token.toString());
        if self.hadError:
            return
        print(ast.AstPrinter().printast(expression))

    def runFile(self, path: str):
        with open(path, "r", encoding="utf-8") as file:
            self.run(file.read())
        if (self.hadError):
            sys.exit(65)
        # TODO handling exceptions here

    def runPrompt(self):
        while True:
            try:
                line = input("> ")
            except EOFError:
                break
            self.run(line)
            self.hadError = False

def cli() -> tp.NoReturn:
    exitCode = Lox(sys.argv)
    sys.exit(exitCode)


if __name__ == "__main__":
    cli()
