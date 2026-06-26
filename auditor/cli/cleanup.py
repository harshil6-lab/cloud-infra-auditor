import typer
from rich.console import Console
from rich.table import Table

from auditor.cleanup.ebs_cleanup import dry_run_ebs, execute_ebs
from auditor.cleanup.eip_cleanup import dry_run_eip, execute_eip

console = Console()
cleanup_app = typer.Typer()


@cleanup_app.command()
def ebs(
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Preview volumes that would be deleted."
    ),
    execute: bool = typer.Option(
        False, "--execute", help="delete unattached EBS volumes."
    ),
):

    if dry_run:
        report = dry_run_ebs()

        findings = report["findings"]
        regions = report["regions_scanned"]

        if not findings:
            console.print("[green]No unattached EBS volumes found[/green]")
            return

        table = Table(title="Dry Run - EBS Cleanup")

        table.add_column("Volume ID")
        table.add_column("Size")
        table.add_column("State")
        table.add_column("Region")

        for volume in findings:
            table.add_row(
                volume["VolumeId"],
                str(volume["Size"]),
                volume["State"],
                volume["Region"],
            )

        console.print(table)

        console.print(f"[cyan]Regions Scanned     : [/cyan] {regions}")
        console.print(f"[yellow]Resources Found   :[/yellow] {len(findings)}")
        console.print(f"[yellow]Resources deleted :[/yellow] {0}")
        console.print(f"[yellow]Action            : Preview only [/yellow]")

    if execute:
        report = dry_run_ebs()

        findings = report["findings"]

        if not findings:
            console.print("[green]No Unattached EBS volumes found. [/green]")
            return

        console.print(
            f"[red]Warning![/red] This will permenently delete {len(findings)} unattached EBS volume(s)"
        )

        confirm = typer.confirm("Do you want to continue ?")

        if not confirm:
            console.print("[yellow]Cleanup cancelled.[/yellow]")
            return

        deleted = 0
        failed = 0

        for volume in findings:

            try:
                execute_ebs(volume["VolumeId"], volume["Region"])
                console.print(f"[green]Deleted [/green]{volume['VolumeId']}")
                deleted += 1

            except Exception as e:

                console.print(f"[red]Failed [/red]{volume['VolumeId']}")
                console.print(f"[red]{e}[/red]")
                failed += 1

            console.print()
            console.print("[bold green]Cleanup Summary[/bold green]")
            console.print(f"Deleted : {deleted}")
            console.print(f"Failed  : {failed}")


@cleanup_app.command()
def eip(
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Preview volumes that would be deleted."
    ),
    execute: bool = typer.Option(
        False, "--execute", help="delete unattached EBS volumes."
    ),
):

    if dry_run:
        report = dry_run_eip()

        findings = report["findings"]
        regions = report["regions_scanned"]

        if not findings:
            console.print("[green]No unassociated Elastic IPs found[/green]")
            return

        table = Table(title="Dry Run - Elastic IPs Cleanup")

        table.add_column("Allocation ID")
        table.add_column("Public IP"),
        table.add_column("Region")

        for volume in findings:
            table.add_row(volume["AllocationId"], volume["PublicIp"], volume["Region"])

        console.print(table)

        console.print(f"[cyan]Regions Scanned     : [/cyan] {regions}")
        console.print(f"[yellow]Resources Found   :[/yellow] {len(findings)}")
        console.print(f"[yellow]Resources deleted :[/yellow] {0}")
        console.print(f"[yellow]Action            : Preview only [/yellow]")

    if execute:
        report = dry_run_eip()

        findings = report["findings"]

        if not findings:
            console.print("[green]No Uassociated Elastic IPs found. [/green]")
            return

        console.print(
            f"[red]Warning![/red] This will permenently delete {len(findings)} anassociated Elastic IP(s)"
        )

        confirm = typer.confirm("Do you want to continue ?")

        if not confirm:
            console.print("[yellow]Cleanup cancelled.[/yellow]")
            return

        deleted = 0
        failed = 0

        for volume in findings:

            try:
                execute_eip(volume["AllocationId"], volume["Region"])
                console.print(f"[green]Deleted [/green]{volume['AllocationId']}")
                deleted += 1

            except Exception as e:

                console.print(f"[red]Failed [/red]{volume['AllocationId']}")
                console.print(f"[red]{e}[/red]")
                failed += 1

            console.print()
            console.print("[bold green]Cleanup Summary[/bold green]")
            console.print(f"Deleted : {deleted}")
            console.print(f"Failed  : {failed}")
