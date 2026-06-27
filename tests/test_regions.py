from moto import mock_aws
import boto3

from auditor.aws.regions import get_regions


@mock_aws
def test_get_regions_returns_list():

    ec2 = boto3.client("ec2", region_name="us-east-1")

    regions = get_regions()

    assert isinstance(regions, list)
    assert len(regions) > 0


# resion : to check get_regions() actually gives valid>0 or list of regions instaed of dict or None.
