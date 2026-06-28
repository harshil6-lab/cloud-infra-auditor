import csv
import json

from auditor.reports.csv_exporter import export_csv

def test_csv():
     fake_report = {
          "findings": [
               {
                    "resource_type" : "EBS",
                    "resource_id" : "vol-123",
                    "region" : "us-east-1",
                    "status" : "Unattached",
                    "details" : {
                         "size_gib" : 10,
                         "state" : "available"
                    }
               }
          ]
     }

     path = export_csv(fake_report)

     assert path.exists()
     with open(path,newline="",encoding="utf-8") as file:
        reader = list(csv.reader(file))

        assert reader[0] == [
            "Resource Type" , "Resource ID" , "Region" , "Status" , "Details"
        ]

        assert reader[1][0] == "EBS"
        assert reader[1][1] == "vol-123"
        assert reader[1][2] == "us-east-1"
        assert reader[1][3] == "Unattached"

        details = json.loads(reader[1][4])

        assert details["size_gib"] == 10
        assert details["state"] == "available"