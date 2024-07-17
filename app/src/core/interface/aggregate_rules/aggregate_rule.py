from typing import List
from abc import ABC, abstractmethod
from app.src.core.models.types.orquestrador_message_adapter import OrquestradorMessageAdapter
from app.src.core.models import Event

class IAggregationRule(ABC):

    @abstractmethod
    def apply_rule(self, event_data: OrquestradorMessageAdapter, config_list: List[Event]) -> dict:
        pass
