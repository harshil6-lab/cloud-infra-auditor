import csv
import json
from pathlib import Path

def export_csv(report , filename="audit_report.csv"):
    """
    Export standardized report to CSV.
    """

    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok = True)

    file_path = reports_dir / filename
    
    with open(file_path , "w" , newline="",encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Resource Type" , "Resource ID" , "Region" , "Status" , "Details"])

        for item in report["findings"]:
            writer.writerow(
                [
                    item["resource_type"],
                    item["resource_id"],
                    item["region"],
                    item["status"],
                    json.dumps(item["details"])
                ]
            )

    return file_path