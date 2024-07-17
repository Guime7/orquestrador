from abc import ABC, abstractmethod
from app.src.core.models.types.orquestrador_message_adapter import OrquestradorMessageAdapter

class ITableLogger(ABC):
    @abstractmethod
    def create_stream(self, stream_name: str):
        pass

    @abstractmethod
    def save_log(self, stream_name: str, event: OrquestradorMessageAdapter):
        pass
    