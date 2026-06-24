from auditor.reports.report_generator import generate_report
from auditor.reports.json_exporter import json_export

report = generate_report()
path = json_export(report)

print(path)