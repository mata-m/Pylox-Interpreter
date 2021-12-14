import sys
import typing as tp
import Scanner as sc
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
    
    def report(self, line: int, where: str, message: str):
        print("[line " + line + "] Error" + where + ": " + message)
        self.hadError = True

    @staticmethod
    def error(self, line: int, message: str):
        self.report(line, "", message)

    def run(self, source: str):
        print(source)
        scanner = sc.Scanner(source)
        tokens = scanner.scanTokens()

        # For now just printing the tokens
        for token in tokens:
            print(token.toString());

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
