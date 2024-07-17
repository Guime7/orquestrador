
import boto3
# Typing
from mypy_boto3_sqs.type_defs import MessageTypeDef
from mypy_boto3_logs import CloudWatchLogsClient
from mypy_boto3_events import EventBridgeClient
# Adapter
from app.src.entrypoint.adapter import SQSMessageAdapter
# Core
from app.src.core.application.use_cases.aggregate_event_use_case import AggregateEventUseCase
from app.src.core.models.types.orquestrador_message_adapter import OrquestradorMessageAdapter
# DataProvider
from app.src.dataprovider.services import FileParameterConfig
from app.src.dataprovider.services.aws import CloudWatchTableLogger, EventBridgeEventPublisher

class Orquestrador():
    def __init__(self):

        logs_client: CloudWatchLogsClient = boto3.client("logs", region_name="sa-east-1")
        self.cloudwatch_table_logger = CloudWatchTableLogger(
            client=logs_client, log_group_name="log_group_name")

        events_client: EventBridgeClient = boto3.client("events", region_name="sa-east-1")
        self.eventbridge_event_publisher = EventBridgeEventPublisher(
            client=events_client, event_bus_name="event_bus_name")

        self.file_parameter_config = FileParameterConfig(file_path="app/config.yaml")

        self.aggregate_event = AggregateEventUseCase(
            event_publisher=self.eventbridge_event_publisher,
            table_logger=self.cloudwatch_table_logger,
            parameter_config=self.file_parameter_config
        )

    def processar(self, message: MessageTypeDef):
        mensagem_adapted: OrquestradorMessageAdapter = SQSMessageAdapter.adapt(message["body"])
        self.aggregate_event.execute(mensagem_adapted)
  