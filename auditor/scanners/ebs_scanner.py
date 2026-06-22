from auditor.aws.session import create_session
from auditor.utils.retry import retry_on_throttle

from auditor.aws.regions import get_regions
def scan_unattached_volumes(region:str):
    """
    Scan for Unattached EBS volumes...
    """
    session = create_session()

    ec2 = session.client("ec2",region_name=region)

    response= retry_on_throttle(ec2.describe_volumes)
    
    unattached = []

    for volume in response["Volumes"]:
        if volume["State"] == "available":
            unattached.append({"VolumeId" : volume["VolumeId"], "Size" : volume["Size"] , "State" : volume["State"] , "Region" : volume["Region"]})
        
    return unattached

def scan_all_regions_ebs(profile_name=None):
    findings = []
    regions = get_regions(profile_name)

    for region in regions:
        found_region = scan_unattached_volumes(region)
        findings.extend(found_region)

    return {
        "regions_scanned" : len(regions),
        "findings" : findings   
    }