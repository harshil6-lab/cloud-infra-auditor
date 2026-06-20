import typer
from rich.console import Console
from rich.table import Table
from auditor.scanners.ebs_scanner import scan_unattached_volumes

console = Console()

scan_app = typer.Typer()

@scan_app.command()
def ebs():
    """
    Scan Unattached EBS Volumes..
    """

    volumes = scan_unattached_volumes("ap-south-1")

    if not volumes:
        console.print("[green]No Unattached EBS volumes Found.[/green]")
        return 
    
    table = Table(title="Unattached EBS Volumes")

    table.add_column("Volume_Id")
    table.add_column("Size (GiB)")
    table.add_column("State")
    table.add_column("Region")

    for volume in volumes:
        table.add_row(volume["VolumeId"],str(volume["Size"]),volume["State"],volume["Region"])
    
    console.print(table)