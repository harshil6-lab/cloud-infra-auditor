from unittest.mock import MagicMock, patch
from auditor.cleanup.ebs_cleanup import execute_ebs
from auditor.cleanup.eip_cleanup import execute_eip


@patch("auditor.cleanup.ebs_cleanup.create_session")
def test_execute_ebs(mock_create_session):
    mock_session = MagicMock()
    mock_ec2 = MagicMock()

    mock_create_session.return_value = mock_session
    mock_session.client.return_value = mock_ec2

    mock_ec2.delete_volume.return_value = {"ResponseMetadata": {"HTTPStatusCode": 200}}

    response = execute_ebs("vol-123", "us-east-1")

    mock_session.client.assert_called_once_with("ec2", region_name="us-east-1")
    mock_ec2.delete_volume.assert_called_once_with(VolumeId="vol-123")

    assert response["ResponseMetadata"]["HTTPStatusCode"] == 200


@patch("auditor.cleanup.eip_cleanup.create_session")
def test_execute_eip(mock_create_session):

    mock_session = MagicMock()
    mock_ec2 = MagicMock()

    mock_create_session.return_value = mock_session
    mock_session.client.return_value = mock_ec2

    mock_ec2.release_address.return_value = {
        "ResponseMetadata": {"HTTPStatusCode": 200}
    }

    response = execute_eip("eipalloc-123", "us-east-1")

    mock_session.client.assert_called_once_with("ec2", region_name="us-east-1")
    mock_ec2.release_address.assert_called_once_with(AllocationId="eipalloc-123")

    assert response["ResponseMetadata"]["HTTPStatusCode"] == 200
