from datetime import datetime, timedelta

from auditor.aws.session import create_session
from auditor.utils.retry import retry_on_throttle


def get_average_cpu_utilization(instance_id: str, region: str):
    """
    Get Average CPU utilization Over last 14 days.
    """

    session = create_session()

    cloudwatch = session.client("cloudwatch", region_name=region)

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=14)

    response = retry_on_throttle(
        cloudwatch.get_metric_statistics,
        Namespace="AWS/EC2",
        MetricName="CPUUtilization",
        Dimensions=[{"Name": "InstanceId", "Value": instance_id}],
        StartTime=start_time,
        EndTime=end_time,
        Period=86400,
        Statistics=["Average"],
    )

    return response
