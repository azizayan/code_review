from typing import List
from dataclasses import dataclass
from analyzer import FunctionInfo, ImportInfo

@dataclass
class Issue:
    code: str
    message: str
    lineno: int
    importance: str

def check_docstrings(functions: List[FunctionInfo]):
    issues = []
    for func in functions:
        if not func.docstring:
            issues.append(Issue(
                code="basic standarts ",
                message=f"Function '{func.name}' is missing a docstring.",
                lineno=func.lineno,
                severity="low"
            ))
    return issues

def check_imports_top_level(imports: List[ImportInfo]) -> List[Issue]:
   
    issues = []
    for imp in imports:
        
        if imp.lineno > 50: 
            issues.append(Issue(
                code="hard coded import checks",
                message=f"Late import detected: '{imp.module}'. Move to top of file.",
                lineno=imp.lineno,
                severity="low"
            ))
    return issues

def check_hardcoded_paths(source_code: str) -> List[Issue]:
    
    issues = []
    lines = source_code.splitlines()
    
    
    suspicious_substrings = ["/Users/", "C:/", "D:/", "/home/"]
    
    for i, line in enumerate(lines):
        line_num = i + 1
        
       
        stripped = line.strip()
        if stripped.startswith("#") or stripped.startswith("import") or stripped.startswith("from"):
            continue

       
        
        pass 

    return issues