#Analyzer to parse code into imports and functions
import ast
from pathlib import Path
from dataclasses import dataclass


@dataclass
class FunctionInfo:
    name: str
    lineno: int
    docstring: bool

@dataclass
class ImportInfo:
    module: str
    alias: str | None
    lineno: int

class CodeAnalyzer(ast.NodeVisitor):
    def __init__(self):
       self.stats = {
           "imports" : [],
           "functions" : []
       }

    def visit_Import(self, node):
        for alias in node.names:
                self.stats["imports"].append(ImportInfo( module = alias.name, alias = alias.asname , lineno=node.lineno))
        self.generic_visit(node)
                
            
    def visit_ImportFrom(self, node: ast.ImportFrom):
        mod = node.module or ""
        for alias in node.names:
            if mod : 
               self.stats["imports"].append(
                ImportInfo(module=f"{mod}.{alias.name}", alias=alias.asname or alias.name, lineno=node.lineno))
            else :
                self.stats["imports"].append(
                ImportInfo(module=alias.name, alias=alias.asname or alias.name, lineno=node.lineno))
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        has_doc = ast.get_docstring(node) is not None
        self.stats["functions"].append(FunctionInfo(name= node.name,lineno= node.lineno,docstring=has_doc))
        
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        self.visit_FunctionDef(node)
    



def parse_code(filepath: str | Path):
    """Parse a Pyhton file and return import's and fucntion's names in the file."""
    path = Path(filepath)
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {path}")
    
    source = path.read_text(encoding="utf-8")
    tree= ast.parse(source)
    analyzer = CodeAnalyzer()
    analyzer.visit(tree)
    return analyzer.stats


