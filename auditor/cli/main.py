import typer

from auditor.cli.scan import scan_app
from auditor.cli.report import report_app
from auditor.cli.cleanup import cleanup_app
from auditor.cli.auth import auth_app
from auditor.cli.aws import aws_app
from auditor.cli.report import report_app

app = typer.Typer(help="Cloud Infrastructure Auditor & Cost Optimizer")

app.add_typer(scan_app, name="scan")
app.add_typer(report_app, name="report")
app.add_typer(cleanup_app, name="cleanup")
app.add_typer(auth_app, name="auth")
app.add_typer(aws_app, name="aws")
app.add_typer(report_app, name="report")
app.add_typer(cleanup_app, name="cleanup")

if __name__ == "__main__":
    app()
