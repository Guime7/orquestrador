import json
from mypy_boto3_events.client import EventBridgeClient
from app.src.core.interface.services import IEventPublisher
from app.src.core.models.types.event_layout_adapter import EventLayoutAdapter

class EventBridgeEventPublisher(IEventPublisher):
    def __init__(self, client: EventBridgeClient, event_bus_name: str) -> None:
        self.__client = client
        self.__event_bus_name = event_bus_name
        self.__check_event_bus_exists()

    def __check_event_bus_exists(self) -> bool:
        try:
            self.__client.describe_event_bus(
                Name=self.__event_bus_name
            )
        except self.__client.exceptions.ResourceNotFoundException:
            raise Exception('Event bus does not exist')
        
        return True

    def publish_event(self, event: EventLayoutAdapter):
        result = self.__client.put_events(
            Entries=[
                {
                    'Source': event['Source'],
                    'DetailType': event['DetailType'],
                    'Detail': json.dumps(event['Detail']),
                    'EventBusName': self.__event_bus_name
                }
            ]
        )
        
        if result['FailedEntryCount'] > 0:
            raise Exception(f"Failed to publish event: {result['Entries']}")

