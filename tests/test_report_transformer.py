from auditor.reports.report_transformer import transform_report


def test_transformer():
    #arrange A
    fake_report = {
        "ebs"  : {
            "findings" : [
                {
                    "VolumeId" : "vol-123",
                    "Size"  : 10,
                    "State" : "available",
                    "Region" : "us-east-1"
                }
            ]
        },
        "ec2" : {
            "findings" : []
        },
        "eip" : {
            "findings" : []
        }
    }

    #ACT - A

    result = transform_report(fake_report)

    #Assert - A

    assert "findings" in result
    assert len(result["findings"]) == 1

    item = result["findings"][0]

    assert item["resource_type"] == "EBS"
    assert item["resource_id"] == "vol-123"
    assert item["region"] == "us-east-1"
    assert item["status"] == "Unattached"
    assert item["details"]["size_gib"] == 10
    assert item["details"]["state"] == "available"
