from auditor.scanners.ebs_scanner import scan_all_regions_ebs
from auditor.aws.session import create_session


def dry_run_ebs():
    """
    Preview Unaatached EBS volumes that would be deleted
    """

    report = scan_all_regions_ebs()
    return report


def execute_ebs(volume_id: str, region: str):
    """
    Delete an unattached EBS volume.
    """
    session = create_session()
    ec2 = session.client("ec2", region_name=region)

    response = ec2.delete_volume(VolumeId=volume_id)

    return response
