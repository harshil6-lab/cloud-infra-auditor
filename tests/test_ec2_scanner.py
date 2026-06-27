from unittest.mock import patch
from moto import mock_aws
import boto3

from auditor.scanners.ec2_scanner import scan_idle_instances


@mock_aws
@patch("auditor.scanners.ec2_scanner.get_average_cpu_utilization")
def test_scan_idle_instances(mock_cpu):
    mock_cpu.return_value = {"Datapoints": [{"Average": 2.5}]}
    ec2 = boto3.client("ec2", region_name="us-east-1")

    vpc = ec2.create_vpc(CidrBlock="10.0.0.0/16")
    subnet = ec2.create_subnet(VpcId=vpc["Vpc"]["VpcId"], CidrBlock="10.0.0.1/24")

    ec2.run_instances(
        ImageId="ami-12345678",
        MinCount=1,
        MaxCount=1,
        InstanceType="t2.micro",
        SubnetId=subnet["Subnet"]["SubnetId"],
    )

    instances = scan_idle_instances("us-east-1")

    assert len(instances) == 1
    assert instances[0]["InstanceType"] == "t2.micro"
    assert instances[0]["State"] == "running"
    assert instances[0]["Region"] == "us-east-1"
    assert instances[0]["InstanceId"] is not None
