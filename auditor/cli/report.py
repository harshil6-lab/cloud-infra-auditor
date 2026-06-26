import typer
from rich.console import Console

from auditor.reports.report_generator import generate_report
from auditor.reports.report_transformer import transform_report
from auditor.reports.csv_exporter import export_csv
from auditor.reports.json_exporter import json_export

console = Console()

report_app = typer.Typer()


@report_app.command()
def export(
    format: str = typer.Option(
        "json", "--format", "-f", help="Export format (json/csv)"
    )
):
    raw_report = generate_report()
    report = transform_report(raw_report)

    if format.lower() == "json":
        path = json_export(report)
    elif format.lower() == "csv":
        path = export_csv(report)
    else:
        console.print("[red]Unsupported format[/red]")
        raise typer.Exit()

    console.print()
    console.print("[green]* Report exported successfully! [/green]")
    console.print(f"[cyan]Location :[/cyan] {path}")


@report_app.command()
def generate():
    """
    Generate audit report.
    """
    console.print("[green]Generating report...[/green]")
