from auditor.scanners.ebs_scanner import scan_all_regions_ebs
from auditor.scanners.ec2_scanner import scan_all_regions_ec2
from auditor.scanners.eip_scanner import scan_all_regions_eip


def generate_report():
    eip_result = scan_all_regions_eip()
    ebs_result = scan_all_regions_ebs()
    ec2_result = scan_all_regions_ec2()

    return {"ebs": ebs_result, "ec2": ec2_result, "eip": eip_result}
