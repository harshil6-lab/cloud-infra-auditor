from auditor.reports.report_generator import generate_report
RESOURCE_CONFIG = {
    "EC2" : {
        "id_field" : "InstanceId",
        "status"  :"Idle"
    },
    "EBS" : {
        "id_field" : "VolumeId",
        "status"  :"Unattached"
    },
    "EIP" : {
        "id_field" : "AllocationId",
        "status"  : "Unassociated"
    }, 

}

def build_ec2_details(item):
    return {
        "instance_type" : item["InstanceType"],
        "state" : item["State"]
    }

def build_ebs_details(item):
    return {
        "size_gib" : item["Size"],
        "state"  : item["State"]
    }

def build_eip_details(item):
    return{
        "public_ip" : item["PublicIp"]
    }



def transform_findings(findings:list , resource_type:str , details_builder ):
    """
    Generic Transformer for every scanners.
    """

    config = RESOURCE_CONFIG[resource_type]

    transformed= []

    for item in findings:

        transformed.append(
            {
                "resource_type" : resource_type,
                "resource_id" : item[config["id_field"]],
                "region" : item["Region"],
                "status" : config["status"],
                "details" : details_builder(item)
            }
        )
    
    return transformed


def transform_report(report):
    ec2 = transform_findings(report["ec2"]["findings"],
                       "EC2",
                       build_ec2_details)
    ebs = transform_findings(report["ebs"]["findings"],
                       "EBS",
                       build_ebs_details)
    eip = transform_findings(report["eip"]["findings"],
                       "EIP",
                       build_eip_details)
    
    return {
        "findings" : ec2 + ebs + eip
    }



