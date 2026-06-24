from auditor.scanners.ebs_scanner import scan_unattached_volumes

data = scan_unattached_volumes("ap-south-1")

print(data)
