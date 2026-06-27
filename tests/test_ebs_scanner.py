from moto import mock_aws
import boto3

from auditor.scanners.ebs_scanner import scan_unattached_volumes


@mock_aws
def test_scan_unattached_volumes():
    ec2 = boto3.client("ec2", region_name="us-east-1")  # arrange

    ec2.create_volume(AvailabilityZone="us-east-1a", Size=10)

    volumes = scan_unattached_volumes("us-east-1")  # act

    assert len(volumes) == 1
    assert volumes[0]["Size"] == 10
    assert volumes[0]["State"] == "available"
    assert volumes[0]["VolumeId"] is not None
    assert volumes[0]["Region"] == "us-east-1"
