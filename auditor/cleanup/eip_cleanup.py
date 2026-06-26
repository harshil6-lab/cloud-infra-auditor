from auditor.scanners.eip_scanner import scan_all_regions_eip
from auditor.aws.session import create_session


def dry_run_eip():
    """
    Preview unassociated Elastic IPs that would be released.
    """
    return scan_all_regions_eip()


def execute_eip(allocation_id: str, region: str):
    session = create_session()

    ec2 = session.client("ec2", region_name=region)

    response = ec2.release_address(AllocationId=allocation_id)

    return response
