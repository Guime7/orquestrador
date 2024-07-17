# import pytest
# from moto import mock_aws
# import boto3
# from mypy_boto3_events.client import EventBridgeClient
# from app.src.dataprovider.services.aws.eventbridge_event_publisher import EventBridgePublisher


# @mock_aws
# def test_succeed_publish_event():
#     # create a boto3 client
#     client: EventBridgeClient = boto3.client("events", region_name="us-east-1")
#     # create event bus
#     client.create_event_bus(Name="event_bus_name")

#     # instance of EventBridgePublisher
#     eventbridge_publisher = EventBridgePublisher(client, "event_bus_name")

#     event = {"source": "source", "detail_type": "detail_type", "detail": {}}

#     eventbridge_publisher.publish_event(event)


# @mock_aws
# def test_when_event_bus_not_exist_raise_exception():
#     # create a boto3 client
#     client: EventBridgeClient = boto3.client("events", region_name="us-east-1")

#     try:
#         EventBridgePublisher(client, "not_exist_event_bus_name")
#         assert False
#     except Exception as e:
#         assert str(e) == "Event bus does not exist"


# @mock_aws
# def test_failed_publish_event_with_rejected_event_info():
#     # create a boto3 client
#     client: EventBridgeClient = boto3.client("events", region_name="us-east-1")
#     client.create_event_bus(Name="event_bus_name")

#     # instance of EventBridgePublisher
#     eventbridge_publisher = EventBridgePublisher(client, "event_bus_name")

#     # mock put_events
#     with pytest.raises(Exception) as e:
#         eventbridge_publisher.publish_event({"source": "", "detail_type": "detail_type", "detail": {}})

#     assert (
#         str(e.value)
#         == "Failed to publish event: [{'ErrorCode': 'InvalidArgument', 'ErrorMessage': 'Parameter Source is not valid. Reason: Source is a required argument.'}]"
#     )
