import typer
from rich.console import Console

console = Console()

report_app = typer.Typer()

@report_app.command()
def generate():
    """
    Generate audit report.
    """
    console.print("[green]Generating report...[/green]")