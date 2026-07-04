from auditor.aws.session import create_session
from auditor.utils.retry import retry_on_throttle

from auditor.aws.regions import get_regions

from concurrent.futures import ThreadPoolExecutor, as_completed


def scan_unattached_volumes(region: str):
    """
    Scan for Unattached EBS volumes...
    """
    session = create_session()

    ec2 = session.client("ec2", region_name=region)

    response = retry_on_throttle(ec2.describe_volumes)

    unattached = []

    for volume in response["Volumes"]:
        if volume["State"] == "available":
            unattached.append(
                {
                    "VolumeId": volume["VolumeId"],
                    "Size": volume["Size"],
                    "State": volume["State"],
                    "Region": region,
                }
            )

    return unattached


def scan_all_regions_ebs(profile_name=None):
    findings = []

    regions = get_regions(profile_name)

    with ThreadPoolExecutor(max_workers=min(8, len(regions))) as executor:
        future_to_region = {}
        for region in regions:
            future = executor.submit(scan_unattached_volumes, region)
            future_to_region[future] = region

        for future in as_completed(future_to_region):
            region = future_to_region[future]
            try:
                unattached_volumes = future.result()
                findings.extend(unattached_volumes)
            except Exception as e:
                print(f"[red]Error scanning region {region}: {e}[/red]")

    return {"regions_scanned": len(regions), "findings": findings}
