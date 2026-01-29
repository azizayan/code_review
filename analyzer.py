#Analyzer to parse code into imports and functions
import ast
from pathlib import Path



def parse_code(filepath: str | Path) -> dict[str, list[str]]:
    """Parse a Pyhton file and return import's and fucntion's names in the file."""
    path = Path(filepath)
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {path}")
    
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=(path))


    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update( alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            for alias in node.names:
                if mod:
                    imports.add(f"{mod}.{alias.name}")
                else: 
                    imports.add(alias.name)
            
    functions = [
        node.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]

    return{
        "imports": sorted(imports),
        "functions": functions,
    }


