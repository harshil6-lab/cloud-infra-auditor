from auditor.aws.session import create_session
from auditor.utils.retry import retry_on_throttle


def get_regions(profile_name=None):
    """
    Return ALL available AWS regions.
    """
    session = create_session(profile_name)
    ec2 = session.client("ec2")

    response = retry_on_throttle(ec2.describe_regions)

    return [region["RegionName"] for region in response["Regions"]]
