
base_desc = {
    "Expr": {
        "Unary": [["Scanner.Token", "operator"], ["Expr", "right"]],
        "Binary": [["Expr", "left"], ["Scanner.Token", "operator"], ["Expr", "right"]],
        "Grouping" : [["Expr", "expression"]],
        "Literal" : [["object", "value"]]
    }
}

tab = "    "

def defineType(outputDir, baseName, className, fieldList):
    # Splitting into types and names
    types, names = zip(*fieldList)
    # Joining field names
    fieldStr = ", ".join(names)

    param_stmts = [tab + tab +
                   "self." + field[1] + " = " + field[1] + "\n"
                   for field in fieldList ]

    assert_stmts = [tab + tab + 
                   "assert isinstance(" + field[1] + ", " + field[0] + ")\n"
                   for field in fieldList]

    outputDir.write("\n")
    # Class
    outputDir.writelines(["class " + className + "(" + baseName + "):\n",
                          "",
                          # Constructor
                          tab + "def __init__(self, " + fieldStr +"):\n"])
    # Asserts
    outputDir.writelines(assert_stmts)
    outputDir.write("\n")
    # Store parameters
    outputDir.writelines(param_stmts)
    outputDir.write("\n")
    # Write accept methods for visitor pattern
    outputDir.write(tab + "def accept(self, visitor):\n" + 
                    tab + tab + "return visitor.visit" + className + baseName + "(self)\n")

def defineVisitor(outputDir, baseName: str, types: list[str]):
    outputDir.write("class Visitor:\n")
    
    type_stmts = [tab + "def visit" + expr_type + baseName + "(" +
                  expr_type.lower() + baseName  + "):\n" + tab + tab + "pass\n" for expr_type, fields in types.items()]
    outputDir.writelines(type_stmts)


def defineAst(outputDir, baseName: str, types: list[str]):
    outputDir.write("import Scanner\n\n\n")
    outputDir.writelines(["class " + baseName + ":\n",
                           tab + "pass\n\n"])
    defineVisitor(outputDir, baseName, types)

    # The AST classes.
    for expr_type, fields in types.items():
        defineType(outputDir, baseName, expr_type, fields)
    
    



if __name__ == "__main__":
    path = "../Expr.py"
    with open(path, "w+") as outputDir:
        defineAst(outputDir, "Expr", base_desc["Expr"])