from abc import ABC, abstractmethod
# from models.event import Event

class IParameterConfig(ABC):

    @abstractmethod
    def get_all_config(self):
        pass