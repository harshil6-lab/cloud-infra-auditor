import boto3
from botocore.exceptions import NoCredentialsError
from auditor.aws.session import create_session

def list_profiles():
    session = boto3.Session()
    return session.available_profiles   

def get_identity(profile_name=None):
    try:
        """
        Return current caller identity
        """

        session = create_session(profile_name)

        sts = session.client("sts")

        return sts.get_caller_identity()
    
    except NoCredentialsError:
        return  {"error":"AWS credentials not configured"}