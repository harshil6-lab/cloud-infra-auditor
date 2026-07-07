import typer
from rich.console import Console
import time

from auditor.scanners.ebs_scanner import scan_all_regions_ebs
from auditor.scanners.eip_scanner import scan_all_regions_eip
from auditor.scanners.ec2_scanner import scan_all_regions_ec2

from auditor.ui.summary import display_summary

console = Console()

scan_app = typer.Typer()


@scan_app.command()
def ebs():
    """
    Scan Unattached EBS Volumes..
    """
    start_time = time.time()

    volumes = scan_all_regions_ebs()

    duration = time.time() - start_time

    findings = volumes["findings"]
    regions_scanned = volumes["regions_scanned"]

    if not findings:
        console.print("[green]✓ No unattached EBS volumes found.[/green]")
        console.print()
        display_summary(
            regions_scanned=regions_scanned,
            resource_found=len(findings),
            duration=duration,
            resource_name="Elastic Block Storage",
        )
        return
    console.print("[bold green]✓ Scan completed successfully.[/bold green]")
    console.print()
    console.print(
        f"[bold yellow]⚠ Found {len(findings)} Unattached EBS Volume(s).[/bold yellow]"
    )
    console.print()

    display_summary(
        regions_scanned=regions_scanned,
        resource_found=len(findings),
        duration=duration,
        resource_name="Elastic Block Storage",
    )


@scan_app.command()
def eip():
    """
    Scan Unassociated Elastic IPs...
    """
    start_time = time.time()
    volumes = scan_all_regions_eip()

    duration = time.time() - start_time

    findings = volumes["findings"]
    regions_scanned = volumes["regions_scanned"]

    if not findings:
        console.print("[green]✓ No unassociated Elastic IPs found.[/green]")
        display_summary(
            regions_scanned=regions_scanned,
            resource_found=len(findings),
            duration=duration,
            resource_name="Elastic IPs",
        )
        return
    console.print("[bold green]✓ Scan completed successfully.[/bold green]")
    console.print()
    console.print(
        f"[bold yellow]⚠ Found {len(findings)} Unasssociated Elastic IP(s).[/bold yellow]"
    )
    console.print()

    display_summary(
        regions_scanned=regions_scanned,
        resource_found=len(findings),
        duration=duration,
        resource_name="Elastic IPs",
    )


@scan_app.command()
def ec2():
    """
    Scan Idle EC2 Instances...
    """
    start_time = time.time()
    volumes = scan_all_regions_ec2()

    duration = time.time() - start_time

    findings = volumes["findings"]
    regions_scanned = volumes["regions_scanned"]

    if not findings:
        console.print("[green]✓ No Idle EC2 Instances found.[/green]")
        display_summary(
            regions_scanned=regions_scanned,
            resource_found=len(findings),
            duration=duration,
            resource_name="Idle EC2 Instances",
        )
        return
    console.print("[bold green]✓ Scan completed successfully.[/bold green]")
    console.print()
    console.print(
        f"[bold yellow]⚠ Found {len(findings)} idle EC2 instance(s).[/bold yellow]"
    )
    console.print()

    display_summary(
        regions_scanned=regions_scanned,
        resource_found=len(findings),
        duration=duration,
        resource_name="Idle EC2 Instances",
    )
