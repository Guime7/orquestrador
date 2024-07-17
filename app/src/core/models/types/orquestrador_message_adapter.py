from typing import List, TypedDict

OrquestradorMessageAdapter = TypedDict(
    "OrquestradorMessageAdapter",
    {
        "TableName": str,
        "DatabaseName": str,
        "Partitions": List[str],
        "StepFunctionID": str
    },
)

