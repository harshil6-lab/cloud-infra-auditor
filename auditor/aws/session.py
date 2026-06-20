import boto3

def create_session(profile_name=None):
    """
    Create boto3 Session.
    """

    if profile_name:
        return boto3.Session(profile_name=profile_name)
    
    return boto3.Session()