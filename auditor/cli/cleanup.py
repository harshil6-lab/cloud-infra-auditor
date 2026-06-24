import typer
from rich.console import Console

console = Console()
cleanup_app = typer.Typer()


@cleanup_app.command()
def execute():
    """
    Cleanup resources
    """
    console.print("[green]Cleanup intialiated...[/green]")
