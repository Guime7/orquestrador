# pylint: disable=E1101:no-member
# pylint: disable=W0621:redefined-outer-name

import json
from unittest.mock import call
import pytest
from moto import mock_aws
from app.src.entrypoint.orquestrador import Orquestrador

# Adapter
from app.src.entrypoint.adapter import SQSMessageAdapter
from app.src.core.models.types.orquestrador_message_adapter import OrquestradorMessageAdapter

# Core
from app.src.core.application.use_cases.aggregate_event_use_case import AggregateEventUseCase

# DataProvider
from app.src.dataprovider.services import FileParameterConfig
from app.src.dataprovider.services.aws import CloudWatchTableLogger, EventBridgeEventPublisher


@pytest.fixture(name="mock_sqs_message", scope="module")
def mock_sqs_message():
    with open("tests/fixtures/mock_sqs_message.json", "r", encoding="utf-8") as file:
        return json.load(file)


@pytest.fixture(name="mock_orquestrador_message_adapter", scope="module")
def mock_orquestrador_message_adapter() -> OrquestradorMessageAdapter:
    return {
        "TableName": "tabela1",
        "DatabaseName": "database1",
        "Partitions": "part1,part2",
        "StepFunctionID": "step1"
    }


@mock_aws
def test_orquestrador_processar(mocker, mock_sqs_message, mock_orquestrador_message_adapter):

    mocker.patch.object(AggregateEventUseCase, "__init__", return_value=None)
    mocker.patch.object(AggregateEventUseCase, "execute", return_value=None)

    mocker.patch.object(SQSMessageAdapter, "__init__", return_value=None)
    mocker.patch.object(SQSMessageAdapter, "adapt", return_value=mock_orquestrador_message_adapter)

    mocker.patch.object(FileParameterConfig, "__init__", return_value=None)
    mocker.patch.object(CloudWatchTableLogger, "__init__", return_value=None)
    mocker.patch.object(EventBridgeEventPublisher, "__init__", return_value=None)

    event = mock_sqs_message

    orquestrador = Orquestrador()
    orquestrador.processar(event["Records"][0])

    SQSMessageAdapter.adapt.assert_has_calls([call(event["Records"][0]["body"])])
    AggregateEventUseCase.execute.assert_has_calls([call(mock_orquestrador_message_adapter)])
