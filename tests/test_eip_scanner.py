from moto import mock_aws
import boto3

from auditor.scanners.eip_scanner import scan_unattached_eips


@mock_aws
def test_scan_unattached_eips():

    ec2 = boto3.client("ec2", region_name="us-east-1")

    ec2.allocate_address(Domain="vpc")

    eips = scan_unattached_eips("us-east-1")

    assert len(eips) == 1
    assert eips[0]["AllocationId"] is not None
    assert eips[0]["PublicIp"] is not None
    assert eips[0]["Region"] == "us-east-1"
    assert len(eips[0]) == 3
