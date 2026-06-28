#Arrange

from unittest.mock import patch
from auditor.reports.report_generator import generate_report

@patch("auditor.reports.report_generator.scan_all_regions_ebs")
@patch("auditor.reports.report_generator.scan_all_regions_eip")
@patch("auditor.reports.report_generator.scan_all_regions_ec2")

def test_generate_report(mock_ec2,mock_eip,mock_ebs):
    mock_ebs.return_value = {
        "regions_scanned" : 17,
        "findings" : [{
            "volumeId" : "vol-123",
            "Size" : 10,
            "State" : "available",
            "Region" : "us-east-1"
        }]
    }

    mock_ec2.return_value = {
        "regions_scanned" : 17,
        "findings" : []
    }

    mock_eip.return_value = {
        "regions_scanned" : 17,
        "findings" : []
    }

    #act
    report = generate_report()
    assert "ebs" in report
    assert "ec2" in report
    assert "eip" in report 

    assert report["ebs"]["regions_scanned"] == 17
    assert report["eip"]["regions_scanned"] == 17
    assert report["ec2"]["regions_scanned"] == 17
    assert len(report["ebs"]["findings"]) == 1
    assert report["ec2"]["findings"] == []
    assert report["eip"]["findings"] == []
