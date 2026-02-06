from typing import List, Dict, Any
from dataclasses import dataclass


try:
    from .analyzer import FunctionInfo, ImportInfo
except ImportError:
    from analyzer import FunctionInfo, ImportInfo

@dataclass
class Issue:
    lineno: int
    code: str      
    message: str
    severity: str 

def check_docstrings(functions: List[FunctionInfo]) -> List[Issue]:
    issues = []
    for func in functions:
        if not func.docstring:
            issues.append(Issue(
                lineno=func.lineno,
                code="DOC001",  
                message=f"Function '{func.name}' is missing a docstring.",
                severity="low"
            ))
    return issues

def check_imports_top_level(imports: List[ImportInfo]) -> List[Issue]:
    issues = []
    for imp in imports:
        if imp.lineno > 50: 
            issues.append(Issue(
                lineno=imp.lineno,
                code="IMP001",
                message=f"Late import detected: '{imp.module}'. Move to top of file.",
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

        for pattern in suspicious_substrings:
            if pattern in line:
                issues.append(Issue(
                    lineno=line_num,
                    code="SEC001",
                    message=f"Hardcoded path detected ('{pattern}'). Use relative paths or config files.",
                    severity="high"
                ))
                break
    return issues


def check_train_test_split(imports: List[ImportInfo]) -> List[Issue]:
    issues = []
    splitting_tools = {"train_test_split", "KFold", "StratifiedKFold", "TimeSeriesSplit"}
    
    
    has_split = any(any(tool in imp.module for tool in splitting_tools) for imp in imports)
        
    if not has_split:
        issues.append(Issue(
            lineno=1,
            code="ML001",
            message="No data splitting tool detected. Risk of data leakage.",
            severity="high"
        ))

    return issues

def check_reproducibility(source_code: str) -> List[Issue]:
    issues = []
    seed_keywords = ["random_state=", "seed=", "np.random.seed", "torch.manual_seed", "tf.random.set_seed"]

    has_seed = False
    for keyword in seed_keywords:
        if keyword in source_code:
            has_seed = True
            break
        
    if not has_seed:
        issues.append(Issue(
            lineno=1,
            code="REP001",
            message="No random seed detected. Results will not be trustworthy.",
            severity="medium"
        ))

    return issues


def check_experiment_config(facts: Dict) -> List[Issue]:
    issues = []
    
    lr = facts.get('learning_rate')
    if lr is not None:
        try:
            lr_val = float(lr)
            if lr_val > 0.1 or lr_val < 1e-6:
                issues.append(Issue(
                    lineno=1, 
                    code="HYP001",
                    message=f"Learning rate {lr_val} is unusual. Standard range is 1e-5 to 0.1.",
                    severity="medium"
                ))
        except (ValueError, TypeError):
            pass 

    optimizer = str(facts.get('optimizer', '')).lower()
    epochs = facts.get('epochs')
    
    if optimizer and ("adam" in optimizer or "sgd" in optimizer):
        if epochs is not None and isinstance(epochs, int) and epochs < 5:
            issues.append(Issue(
                lineno=1,
                code="HYP002",
                message=f"Epoch count ({epochs}) is very low for a neural network training run.",
                severity="low"
            ))

    return issues