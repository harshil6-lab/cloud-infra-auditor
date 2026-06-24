import typer
from rich.console import Console
from rich.table import Table
import time

from auditor.scanners.ebs_scanner import scan_all_regions_ebs
from auditor.scanners.eip_scanner import scan_all_regions_eip
from auditor.scanners.ec2_scanner import scan_all_regions_ec2

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
        table.add_row(
            volume["VolumeId"], str(volume["Size"]), volume["State"], volume["Region"]
        )

    console.print(table)
    console.print(f"[cyan]Regions Scanned : [/cyan] {regions_scanned}")
    console.print(f"[cyan]Volumes Found   : [/cyan] {len(findings)}")
    console.print(f"[cyan]Scan Duartion   : [/cyan] {duration:.2f} sec")


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
        console.print("[green]No Unassociated Elastic IPs Found[/green]")
        console.print(f"Regions Scanned : {regions_scanned}")
        console.print(f"Scan Duartion : {duration:.2f}")
        return

    table = Table(title="Unassociated Elastic IPs")

    table.add_column("Public IP")
    table.add_column("Allocation ID")
    table.add_column("Region")

    for eip in findings:
        table.add_row(eip["PublicIp"], eip["AllocationId"], eip["Region"])

    console.print(table)
    console.print(f"[cyan]Regions Scanned : [/cyan] {regions_scanned}")
    console.print(f"[cyan]Elastic IPs Found : [/cyan] {len(findings)}")
    console.print(f"[cyan]Scan Duartion : [/cyan] {duration:.2f} sec ")


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
        console.print("[green]No Idle EC2 Instances are Found[/green]")
        console.print(f"Regions Scanned : {regions_scanned}")
        console.print(f"Scan Duartion : {duration:.2f}")
        return

    table = Table(title="Idle EC2 Instances")

    table.add_column("Instance ID")
    table.add_column("Instance Type")
    table.add_column("State")
    table.add_column("Region")

    for ec2 in findings:
        table.add_row(
            ec2["InstanceId"], ec2["InstanceType"], ec2["State"], ec2["Region"]
        )

    console.print(table)
    console.print(f"[cyan]Regions Scanned : [/cyan] {regions_scanned}")
    console.print(f"[cyan]Idle EC2 Instances Found : [/cyan] {len(findings)}")
    console.print(f"[cyan]Scan Duartion : [/cyan] {duration:.2f} sec ")
