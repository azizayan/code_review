from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown
from rich.progress import Progress, TextColumn
import time

console = Console()

def print_banner():
    console.print(Panel.fit(
        "[bold red]AI-Powered ML Code Reviewer[/bold red]\n"
        "[dim]v0.1 | Architecture • Logic • Data Hygiene[/dim]",
        border_style="bold red"
    ))

def show_processing_system(description: str, task_func):
    with Progress(
        TextColumn("[bold green]{task.description}"),
        transient=True
    ) as progress:
        progress.add_task(description=description, total=None)
        result = task_func()
        return result
    
def print_code_issues(issues):
    if not issues:
        console.print("[bold green]✨ Code Check Passed: No issues found![/bold green]")
        return
    
    table = Table(title=f"Found {len(issues)} Issues", show_header=True, header_style="bold_red")
    table.add_column("Line", style="dim", width=6)
    table.add_column("Severity", width=10)
    table.add_column("Code", width=8)

    for issue in issues:
        if issue.severity == "high":
            sev_style = "[red]HIGH[/red]"
        elif issue.severity == "medium":
            sev_style = "[yellow]MED[/yellow]"
        else:
            sev_style = "[blue]LOW[/blue]"
            
        table.add_row(
            str(issue.lineno),
            sev_style,
            issue.code,
            issue.message
        )

    console.print(table)
    console.print("\n")


