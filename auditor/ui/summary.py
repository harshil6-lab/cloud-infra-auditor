from rich.table import Table
from rich.console import Console
from rich.panel import Panel


def display_summary(
    *,
    regions_scanned: int,
    resource_found: int,
    duration: float,
    resource_name: str = "Resources",
) -> None:
    if regions_scanned:
        avg_time = duration / regions_scanned
    else:
        avg_time = 0

    console = Console()
    summary_table = Table.grid()

    summary_table.add_column(style="bold white")
    summary_table.add_column(justify="right", style="bold green")

    summary_table.add_row("Regions Scanned", str(regions_scanned))
    summary_table.add_row("Findings", str(resource_found))
    summary_table.add_row("Duration", f"{duration:.2f} sec")
    summary_table.add_row(
        "Avg Scan Time",
        f"{avg_time:.2f} sec",
    )

    summary_panel = Panel(
        summary_table,
        title="[bold cyan]Scan Summary[/bold cyan]",
        border_style="green",
        expand=False,
    )
    console.print(summary_panel)
