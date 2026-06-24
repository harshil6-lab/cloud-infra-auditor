import json
from pathlib import Path


def json_export(report: dict, filename: str = "audit_report.json"):
    reports_dict = Path("reports")
    reports_dict.mkdir(exist_ok=True)

    file_path = reports_dict / filename

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)

    return file_path
