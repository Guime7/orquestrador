# pylint: disable=E1102

import yaml
from app.src.core.interface.services import IParameterConfig
from app.src.core.models import Table, Process, Event


class FileParameterConfig(IParameterConfig):
    def __init__(self, file_path):
        self.file_path = file_path

    def __load_config_yaml(self):
        with open(self.file_path, "r", encoding="utf-8") as file:
            return yaml.safe_load(file)

    def _mapping_event(self, event_data):
        try:
            event_processes = [Process(**process) for process in event_data['processes']]
            event_tables = [Table(**table) for table in event_data['tables']]
            return Event(
                id=event_data['id'],
                rule_type=event_data['rule_type'],
                name=event_data['name'],
                processes=event_processes,
                tables=event_tables,
            )
        except Exception as e:
            raise ValueError(f"Error mapping event config: {str(e)}") from e

    def get_all_config(self) -> Event:
        try:
            data = self.__load_config_yaml()
            events = []
            
            for event_data in data['events']:
                event = self._mapping_event(event_data)
                events.append(event)
    
            return events
        except FileNotFoundError as e:
            raise FileNotFoundError(f"File not found: {str(e)}") from e
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Error loading yaml: {str(e)}") from e
        except Exception as e:
            raise ValueError(f"Error loading config: {str(e)}") from e

