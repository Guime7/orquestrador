from typing import TypedDict, Dict, Union
from app.src.core.models.types.orquestrador_message_adapter import OrquestradorMessageAdapter

EventLayoutAdapter = TypedDict(
    "EventLayoutAdapter",
    {
        "Source": str,
        "DetailType": str,
        "Detail": Dict[str, Union[dict, OrquestradorMessageAdapter]],
    },
)  # Add a closing parenthesis here
