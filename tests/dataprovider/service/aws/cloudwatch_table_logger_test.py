import time
from moto import mock_aws
import boto3
import pytest
from mypy_boto3_logs.client import CloudWatchLogsClient
from app.src.dataprovider.services.aws.cloudwatch_table_logger import CloudWatchTableLogger

@mock_aws
def test_when_log_group_not_exist_raise_exception():
    # create a boto3 client
    client: CloudWatchLogsClient = boto3.client("logs", region_name="us-east-1")

    try:
        CloudWatchTableLogger(client, "not_exist_log_group_name")
        assert False
    except Exception as e:
        assert str(e) == "Log group does not exist"


@mock_aws
def test_succeed_save_log_when_stream_not_exist():
    # create a boto3 client
    client: CloudWatchLogsClient = boto3.client("logs", region_name="us-east-1")
    client.create_log_group(logGroupName="log_group_name")

    # instance of CloudWatchTableLogger
    cloudwatch_table_logger = CloudWatchTableLogger(client, "log_group_name")

    # create steam
    cloudwatch_table_logger.create_stream("stream_name")

    # save log
    actual_timestamp = int(time.time() * 1000)
    cloudwatch_table_logger.save_log("stream_name", {"message": "value", "timestamp": actual_timestamp})

    # recuperar log salvo e validar
    response = client.get_log_events(logGroupName="log_group_name", logStreamName="stream_name")

    assert response["events"][0]["message"] == "value"
    assert response["events"][0]["timestamp"] == actual_timestamp

@mock_aws
def test_failed_save_log_with_rejected_event_info():
    # create a boto3 client
    client: CloudWatchLogsClient = boto3.client("logs", region_name="us-east-1")
    client.create_log_group(logGroupName="log_group_name")
    client.create_log_stream(logGroupName="log_group_name", logStreamName="stream_name")

    # instance of CloudWatchTableLogger
    cloudwatch_table_logger = CloudWatchTableLogger(client, "log_group_name")

    # mock put_log_events
    with pytest.raises(Exception) as e:
        cloudwatch_table_logger.save_log("stream_name", {"message": "value", "timestamp": 1})

    assert str(e.value) == "Rejected log events: {'tooOldLogEventEndIndex': 0}"


@mock_aws
def test_succeed_save_log_when_stream_already_exist():
    # create a boto3 client
    client: CloudWatchLogsClient = boto3.client("logs", region_name="us-east-1")
    client.create_log_group(logGroupName="log_group_name")
    client.create_log_stream(logGroupName="log_group_name", logStreamName="stream_name")

    # instance of CloudWatchTableLogger
    cloudwatch_table_logger = CloudWatchTableLogger(client, "log_group_name")

    # save log
    actual_timestamp = int(time.time() * 1000)
    cloudwatch_table_logger.save_log("stream_name", {"message": "value", "timestamp": actual_timestamp})

    # recuperar log salvo e validar
    response = client.get_log_events(logGroupName="log_group_name", logStreamName="stream_name")

    assert response["events"][0]["message"] == "value"
    assert response["events"][0]["timestamp"] == actual_timestamp

@mock_aws
def test_failed_save_log_because_stream_not_exist():
    # create a boto3 client
    client: CloudWatchLogsClient = boto3.client("logs", region_name="us-east-1")
    client.create_log_group(logGroupName="log_group_name")

    # instance of CloudWatchTableLogger
    cloudwatch_table_logger = CloudWatchTableLogger(client, "log_group_name")

    try:
        cloudwatch_table_logger.save_log("stream_name", {"message": "value", "timestamp": 123456789})
        assert False
    except Exception as e:
        assert (
            str(e)
            == "An error occurred (ResourceNotFoundException) when calling the PutLogEvents operation: The specified log stream does not exist."
        )

@mock_aws
def test_create_stream_validate_if_check_stream_exists_was_called(mocker):
    # create a boto3 client
    client: CloudWatchLogsClient = boto3.client("logs", region_name="us-east-1")
    client.create_log_group(logGroupName="log_group_name")

    # instance of CloudWatchTableLogger
    cloudwatch_table_logger = CloudWatchTableLogger(client, "log_group_name")
    mock_check_stream_exists = mocker.patch.object(
        cloudwatch_table_logger, "_CloudWatchTableLogger__check_stream_exists"
    )
    mock_check_stream_exists.return_value = False

    cloudwatch_table_logger.create_stream("stream_name")

    assert mock_check_stream_exists.call_count == 1
    ##verificar retorno no __check_stream_exists
    mock_check_stream_exists.assert_called_with("stream_name")