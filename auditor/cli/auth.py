import typer
from rich.console import Console

from auditor.aws.auth import get_identity
from auditor.aws.auth import list_profiles
console = Console()

auth_app = typer.Typer()

@auth_app.command()
def identity(profile : str = typer.Option(None,"--profile","-p")):
    """
    Show AWS identity.
    """
    
    data = get_identity()
    if "error" in data:
        console.print("[red]AWS credentials not configured[/red]")
        return
    
    console.print({
        "Account" : data["Account"],
        "Arn" : data["Arn"],
        "UserId" : data["UserId"]
    })

@auth_app.command()
def profiles():
    profiles = list_profiles()

    for profile in profiles:
        console.print(f"[green]{profile}[/green]")
