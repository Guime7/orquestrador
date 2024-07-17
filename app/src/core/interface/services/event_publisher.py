from abc import ABC, abstractmethod
from app.src.core.models.types.event_layout_adapter import EventLayoutAdapter

class IEventPublisher(ABC):

    @abstractmethod
    def publish_event(self, event: EventLayoutAdapter):
        pass