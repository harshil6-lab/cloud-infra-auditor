from auditor.reports.json_exporter import json_export
import json

def test_json():
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

    path = json_export(fake_report)

    assert path.exists()
    with open(path) as f: data = json.load(f)
    assert data["ebs"]["findings"][0]["VolumeId"] == "vol-123"
    assert data["ebs"]["findings"][0]["Size"] == 10
    assert data["ebs"]["findings"][0]["State"] == "available"
    assert data["ebs"]["findings"][0]["Region"] == "us-east-1"
    assert data["ec2"]["findings"] == []
    assert data["eip"]["findings"] == []
