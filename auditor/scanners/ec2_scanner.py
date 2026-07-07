from auditor.aws.session import create_session
from auditor.utils.retry import retry_on_throttle

from auditor.aws.cloudwatch import get_average_cpu_utilization
from auditor.utils.parallel import scan_scanners


def get_instances(region: str):
    session = create_session()

    ec2 = session.client("ec2", region_name=region)

    response = retry_on_throttle(ec2.describe_instances)

    instances = []

    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:

            instances.append(
                {
                    "InstanceId": instance["InstanceId"],
                    "State": instance["State"]["Name"],
                    "InstanceType": instance["InstanceType"],
                    "Region": region,
                }
            )
    return instances


def is_idle_instance(instance_id: str, region: str, threshold: float = 5.0):
    metrics = get_average_cpu_utilization(instance_id, region)

    datapoints = metrics["Datapoints"]

    if not datapoints:
        return False

    cpu_values = [point["Average"] for point in datapoints]
    average_cpu = sum(cpu_values) / len(cpu_values)

    return average_cpu < threshold


def scan_idle_instances(region: str):
    instances = get_instances(region)
    findings = []

    for instance in instances:

        if instance["State"] != "running":
            continue

        if is_idle_instance(instance["InstanceId"], region):
            findings.append(instance)

    return findings


def scan_all_regions_ec2(profile_name=None):
    return scan_scanners(
        scan_function=scan_idle_instances,
        profile_name=profile_name,
        task_description="Scanning for Idle EC2 Instances",
    )
