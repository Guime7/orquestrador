# pylint: disable=W0718:broad-exception-caught
# pylint: disable=W0613:unused-argument
# pylint: disable=W0611:unused-import

import json
from typing import Dict, List, Any
from mypy_boto3_sqs.type_defs import MessageTypeDef
from app.src.entrypoint.orquestrador import Orquestrador

def lambda_handler(event: Dict[str, Any], context: Any):

    orquestrador = Orquestrador()

    try:
        records_list: List[MessageTypeDef] = event["Records"]

        for record in records_list:
            # record["Body"] = json.loads(record["Body"])
            orquestrador.processar(record)
    except Exception as error:
        raise error
