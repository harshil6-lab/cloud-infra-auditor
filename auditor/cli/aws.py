import typer
from rich.console import Console
from rich.table import Table

from auditor.aws.regions import get_regions

console = Console()
aws_app = typer.Typer()

@aws_app.command()
def regions():
    """
    List AWS Regions.
    """
    region_list = get_regions()

    table = Table(title = "AWS Regions")
    table.add_column("Region")
    for region in region_list:
        table.add_row(region)
    
    console.print(table)