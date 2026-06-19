from auditor.aws.session import create_session

def get_regions(profile_name=None):
    """
    Return ALL available AWS regions.
    """
    session = create_session(profile_name)
    ec2 = session.client("ec2")
    response = ec2.describe_regions()

    return [region["RegionName"] for region in response["Regions"]]