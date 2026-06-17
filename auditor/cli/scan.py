import typer
from rich.console import Console

console = Console()

scan_app = typer.Typer()

@scan_app.command()
def run():
    """
    Run infrastructure audit scan.
    
    """
    console.print("[green]Scanning cloud resources....[/green]")