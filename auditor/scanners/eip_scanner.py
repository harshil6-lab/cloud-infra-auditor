from auditor.aws.session import create_session
from auditor.utils.retry import retry_on_throttle

from auditor.utils.parallel import scan_scanners


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
    return scan_scanners(
        scan_function=scan_unattached_eips,
        profile_name=profile_name,
        task_description="Scanning for Unattached EIPs",
    )
