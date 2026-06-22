from auditor.aws.session import create_session
from auditor.utils.retry import retry_on_throttle

from auditor.aws.regions import get_regions

def scan_unattached_eips(region :str):
    session = create_session()

    ec2 = session.client("ec2",region_name=region)

    response = retry_on_throttle(ec2.describe_addresses)

    findings=[]

    for address in response["Addresses"]:
        if "AssociationId" not in address:
            findings.append({
                "PublicIp" : address["PublicIp"],
                "AllocationId" : address.get("AllocationId","N/A"),
                "Region" : region
            })
    
    return findings

def scan_all_regions_eip(profile_name=None):
    findings=[]

    regions = get_regions(profile_name)

    for region in regions:
        eips  = scan_unattached_eips(region)
        findings.extend(eips)

    return {
        "regions_scanned" : len(regions),
        "findings" : findings 
    }

