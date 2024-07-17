# pylint: disable=E1101:no-member
# pylint: disable=W0621:redefined-outer-name

import json
from unittest.mock import call
import pytest
from app.src.entrypoint.orquestrador import Orquestrador
from app.lambda_function import lambda_handler

@pytest.fixture(name="mock_sqs_message", scope="module")
def mock_sqs_message():
    with open("tests/fixtures/mock_sqs_message.json", "r", encoding="utf-8") as file:
        return json.load(file)

def test_lambda_start_success(mocker, mock_sqs_message):

    mocker.patch.object(Orquestrador, "__init__", return_value=None)
    mocker.patch.object(Orquestrador, "processar", return_value=None)

    event = mock_sqs_message
    context = None

    lambda_handler(event, context)

    orquestrador = Orquestrador()

    expected_calls = [call(record) for record in event["Records"]]
    orquestrador.processar.assert_has_calls(expected_calls)

def test_lambda_fail_generic_error(mocker, mock_sqs_message):

    mocker.patch.object(Orquestrador, "__init__", return_value=None)
    mocker.patch.object(Orquestrador, "processar", side_effect=Exception("Erro genérico"))

    event = mock_sqs_message
    context = None

    with pytest.raises(Exception):
        lambda_handler(event, context)

    orquestrador = Orquestrador()
    orquestrador.processar.assert_called_once()
    