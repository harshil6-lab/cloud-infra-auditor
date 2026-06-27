import boto3

from auditor.aws.session import create_session


def test_create_session_returns_boto3_session():

    session = create_session()

    assert isinstance(session, boto3.Session)


# asssert : assert is mean to be -> i expect this to be true.
# example : if assert 5>3 -> test passed.
# example : if assert 3>5  -> test failed.
