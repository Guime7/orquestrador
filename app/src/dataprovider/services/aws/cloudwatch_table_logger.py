from mypy_boto3_logs.client import CloudWatchLogsClient
from app.src.core.interface.services import ITableLogger
from app.src.core.models.types.orquestrador_message_adapter import OrquestradorMessageAdapter


class CloudWatchTableLogger(ITableLogger):
    def __init__(self, client: CloudWatchLogsClient, log_group_name: str):
        self.__client = client
        self.__log_group_name = log_group_name
        self.__check_log_group_exists()

    def __check_log_group_exists(self) -> bool:
        response = self.__client.describe_log_groups(
            logGroupNamePrefix=self.__log_group_name
        )
        if len(response['logGroups']) == 0:
            raise Exception('Log group does not exist')
        return True

    def __check_stream_exists(self, stream_name: str) -> bool:
        response = self.__client.describe_log_streams(
            logGroupName=self.__log_group_name,
            logStreamNamePrefix=stream_name
        )
        return len(response['logStreams']) > 0

    def create_stream(self, stream_name: str):
        if not self.__check_stream_exists(stream_name):
            self.__client.create_log_stream(
                logGroupName=self.__log_group_name,
                logStreamName=stream_name
            )
            
    def save_log(self, stream_name: str, event: OrquestradorMessageAdapter) -> None:
        response = self.__client.put_log_events(
            logGroupName=self.__log_group_name,
            logStreamName=stream_name,
            logEvents=[
                {
                    'message': event['message'],
                    'timestamp': event['timestamp']
                }
            ]
        )

        if 'rejectedLogEventsInfo' in response:
            raise Exception(f"Rejected log events: {response['rejectedLogEventsInfo']}")
