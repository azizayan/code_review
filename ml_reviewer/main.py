import argparse
from pathlib import Path
import sys
from . import ui
from . import analyzer
from . import checks
from . import extractor

try:
    from . import data_advisor
except ImportError:
    data_advisor = None

def run_analysis(code_path, data_path=None):
    
    ui.print_banner()
    
   
    ui.console.rule("[bold]Phase 1: Code Architecture[/bold]")
    
    
    def run_static_checks():
        try:
            source = Path(code_path).read_text(encoding="utf-8")
            stats = analyzer.parse_code(code_path)
            
            issues = []
            issues.extend(checks.check_docstrings(stats['functions']))
            issues.extend(checks.check_imports_top_level(stats['imports']))
            issues.extend(checks.check_hardcoded_paths(source))
            issues.extend(checks.check_train_test_split(stats['imports']))
            issues.extend(checks.check_reproducibility(source))
            return source, issues
        except FileNotFoundError:
            return None, "File not found."
        except Exception as e:
            return None, str(e)

    
    source_code, result = ui.show_step("Running Static Analysis...", run_static_checks)
    
    if source_code is None:
        ui.console.print(f"[bold red]Fatal Error:[/bold red] {result}")
        return

    all_issues = result

    
    def run_ai_checks():
        facts = extractor.extract_ml_facts(source_code)
        if facts:
            return checks.check_experiment_config(facts)
        return []

   
    ai_issues = ui.show_step("Consulting Local AI (Deep Scan)...", run_ai_checks)
    all_issues.extend(ai_issues)
    
    
    ui.print_code_issues(all_issues)


    if data_path:
        if data_advisor is None:
            ui.console.print("[yellow]Skipping Data Review (data_advisor.py missing)[/yellow]")
            return

        ui.console.print("\n") 
        ui.console.rule("[bold]Phase 2: Data Hygiene[/bold]")
        
       
        def run_data_profile():
            return data_advisor.get_dataset_profile(data_path)
        
       
        profile = ui.show_step("Profiling Dataset Vitals...", run_data_profile)
        ui.print_data_profile(profile)
        
        
        if profile.get("issues"):
            def run_advice():
                return data_advisor.get_cleaning_advice(profile)
            
            advice = ui.show_step("Generating Cleaning Recipe...", run_advice)
            ui.print_ai_advice(advice)


def main_cli_entry_point():
    parser = argparse.ArgumentParser(description="AI-Powered ML Code Reviewer")
    parser.add_argument("code_file", help="Path to Python script")
    parser.add_argument("--data", help="Path to CSV dataset (optional)")
    
    args = parser.parse_args()
    run_analysis(args.code_file, args.data)

if __name__ == "__main__":
    main_cli_entry_point()