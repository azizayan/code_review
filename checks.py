from typing import List
from dataclasses import dataclass
from analyzer import FunctionInfo, ImportInfo

@dataclass
class Issue:
    name: str
    message: str
    lineno: int
    importance: str

def check_docstrings(functions: List[FunctionInfo]):
    issues = []
    for func in functions:
        if not func.docstring:
            issues.append(Issue(
                name="basic standarts",
                message=f"Function '{func.name}' is missing a docstring.",
                lineno=func.lineno,
                importance="low"
            ))
    return issues

def check_imports_top_level(imports: List[ImportInfo]) -> List[Issue]:
   
    issues = []
    for imp in imports:
        
        if imp.lineno > 50: 
            issues.append(Issue(
                name="hard coded import checks",
                message=f"Late import detected: '{imp.module}'. Move to top of file.",
                lineno=imp.lineno,
                importance="low"
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

        for pattern in suspicious_substrings:
            if pattern in line:
                issues.append(Issue(
                    name= "security error",
                    message=f"Hardcoded path detected ('{pattern}'). Use relative paths or config files.",
                    lineno=line_num,
                    importance="high"
                ))
                break
            

    return issues


def check_train_test_split(imports: List[ImportInfo]):
    issues = []
    splitting_tools = {"train_test_split", "KFold", "StratifiedKFold", "TimeSeriesSplit"}

    split_tool_found = False

    for imp in imports:
        if any(tool in imp.module for tool in splitting_tools):
                found_split = True
                break
        
    if not split_tool_found:
        issues.append(Issue(
            name="split error",
            message="No data splitting tool detected. Risk of data leakage.",
            lineno= 1,
            importance="high"

        ))

    return issues

def check_reproducibility(source_code:str):
    issues = []
    seed_keywords = ["random_state=", "seed=", "np.random.seed", "torch.manual_seed", "tf.random.set_seed"]


    has_seed = False
    for keyword in seed_keywords:
        if keyword in source_code:
            has_seed = True
        
        if not has_seed:
            issues.append(Issue(
                name="non reproducable",
                message="No random seed detected. Results will not be trustworthy.",
                lineno=1,
                importance="medium"
            ))

        return issues
    

