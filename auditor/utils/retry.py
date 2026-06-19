from time import sleep
from botocore.exceptions import ClientError
from auditor.constants import MAX_RETRIES 

def retry_on_throttle(func, *args , **kwargs):
    """
    Retry AWS API calls when throttled.
    """

    for attempt in range(MAX_RETRIES):

        try:
            return func(*args,**kwargs)
        
        except ClientError as e:
            error_code = e.response["Error"]["Code"]

            if error_code in ["Throttling","ThrottlingException","RequestLimitExceeded0"]:
                wait_time = 2 ** attempt

                sleep(wait_time)

                continue
            raise
    raise Exception("Maximum retry attempts exceeded.")
                