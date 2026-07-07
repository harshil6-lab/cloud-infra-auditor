from auditor.aws.session import create_session
from auditor.utils.retry import retry_on_throttle
from auditor.utils.parallel import scan_scanners


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
    return scan_scanners(
        scan_function=scan_unattached_volumes,
        profile_name=profile_name,
        task_description="Scanning for Unattached EBS Volumes",
    )
