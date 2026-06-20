from auditor.aws.session import create_session
from auditor.utils.retry import retry_on_throttle
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