import typer
from rich.console import Console
from rich.table import Table
import time

from auditor.scanners.ebs_scanner import scan_all_regions 

console = Console()

scan_app = typer.Typer()

@scan_app.command()
def ebs():
    """
    Scan Unattached EBS Volumes..
    """
    start_time = time.time()

    volumes = scan_all_regions()
    
    duration = time.time() - start_time
    
    findings= volumes["findings"]
    regions_scanned = volumes["regions_scanned"]

    if not findings:
        console.print("[green]No Unattached EBS volumes Found.[/green]")
        
        console.print(f"Regions Scanned : {regions_scanned}")
        console.print(f"Scan Duration : {duration:.2f} sec")
        return


    
    table = Table(title="Unattached EBS Volumes")

    table.add_column("Volume_Id")
    table.add_column("Size (GiB)")
    table.add_column("State")
    table.add_column("Region")

    for volume in findings:
        table.add_row(volume["VolumeId"],str(volume["Size"]),volume["State"],volume["Region"])
    
    console.print(table)
    console.print(f"[cyan]Regions Scanned : [/cyan] {regions_scanned}")
    console.print(f"[cyan]Volumes Found   : [/cyan] {len(findings)}")
    console.print(f"[cyan]Scan Duartion   : [/cyan] {duration:.2f} sec")