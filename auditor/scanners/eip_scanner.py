from auditor.aws.session import create_session
from auditor.utils.retry import retry_on_throttle

from auditor.aws.regions import get_regions

from concurrent.futures import ThreadPoolExecutor, as_completed


def scan_unattached_eips(region: str):
    session = create_session()

    ec2 = session.client("ec2", region_name=region)

    response = retry_on_throttle(ec2.describe_addresses)

    findings = []

    for address in response["Addresses"]:
        if "AssociationId" not in address:
            findings.append(
                {
                    "PublicIp": address["PublicIp"],
                    "AllocationId": address.get("AllocationId", "N/A"),
                    "Region": region,
                }
            )

    return findings


def scan_all_regions_eip(profile_name=None):
    findings = []

    regions = get_regions(profile_name)
    with ThreadPoolExecutor(max_workers=min(8, len(regions))) as executor:
        future_to_region = {}
        for region in regions:
            future = executor.submit(scan_unattached_eips, region)
            future_to_region[future] = region

        for future in as_completed(future_to_region):
            region = future_to_region[future]
            try:
                unattached_eips = future.result()
                findings.extend(unattached_eips)
            except Exception as e:
                print(f"[red]Error scanning region {region}: {e}[/red]")

    return {"regions_scanned": len(regions), "findings": findings}
