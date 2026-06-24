from auditor.aws.cloudwatch import get_average_cpu_utilization

data = get_average_cpu_utilization("i-07d35dab87be9a674", "us-east-1")
print(data)
