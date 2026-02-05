import sys
import argparse
from pathlib import Path
from ml_reviewer.analyzer import parse_code
from ml_reviewer import checks
from ml_reviewer import extractor
from ml_reviewer import ui
from . import data_advisor


def analyze_file(filepath: str):
    ui.print_banner()
    
    
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




def main_cli_entry_point():
    parser = argparse.ArgumentParser(description="AI-Powered ML Code Reviewer")
    parser.add_argument("code_file", help="Path to Python script")
    parser.add_argument("--data", help="Path to CSV dataset (optional)")

    args= parser.parse_args()
    analyze_file(args.code_file)

if __name__ == "__main__":
    main_cli_entry_point()
