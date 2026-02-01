import sys
from pathlib import Path
from analyzer import parse_code
import checks

def analyze_file(filepath: str):
    print(f"Analyzing {filepath}...\n")
    
    
    try:
        path = Path(filepath)
        source_code = path.read_text(encoding="utf-8")
        stats = parse_code(filepath)
    except Exception as e:
        print(f" Error reading file: {e}")
        return

    
    all_issues = []
    
   
    all_issues.extend(checks.check_docstrings(stats['functions']))
    all_issues.extend(checks.check_hardcoded_paths(source_code))
    all_issues.extend(checks.check_train_test_split(stats['imports']))
    all_issues.extend(checks.check_reproducibility(source_code))
    
    
    if not all_issues:
        print("No issues found! Clean code.")
        return

    
    all_issues.sort(key=lambda x: x.lineno)
    
    print(f"Found {len(all_issues)} issues:\n")
    for issue in all_issues:
        # Simple color coding
        icon = "🔴" if issue.importance == "high" else "🟡"
        print(f"{icon} [Line {issue.lineno}] {issue.name}: {issue.message}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <your_script.py>")
    else:
        analyze_file(sys.argv[1])