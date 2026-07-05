from auditor.aws.session import create_session
from auditor.utils.retry import retry_on_throttle

from auditor.aws.regions import get_regions
from auditor.aws.cloudwatch import get_average_cpu_utilization

from concurrent.futures import ThreadPoolExecutor, as_completed


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
    findings = []
    regions = get_regions(profile_name)

    with ThreadPoolExecutor(max_workers=min(8, len(regions))) as executor:
        future_to_region = {}

        for region in regions:
            future = executor.submit(scan_idle_instances, region)
            future_to_region[future] = region

        for future in as_completed(future_to_region):
            region = future_to_region[future]
            try:
                idle_instances = future.result()
                findings.extend(idle_instances)
            except Exception as e:
                print(f"[red]Error scanning region {region}: {e}[/red]")

    return {"regions_scanned": len(regions), "findings": findings}
