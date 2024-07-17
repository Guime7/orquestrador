from typing import List
from app.src.core.interface.services import IParameterConfig, ITableLogger, IEventPublisher
from app.src.core.models import Event
from app.src.core.models.types.orquestrador_message_adapter import OrquestradorMessageAdapter
from app.src.core.models.types.event_layout_adapter import EventLayoutAdapter
from app.src.core.application.aggregate_rules.one_table_rule import OneTableRule

class AggregateEventUseCase:
    def __init__(self, 
                 event_publisher: IEventPublisher, 
                 table_logger: ITableLogger, 
                 parameter_config: IParameterConfig):
        self.parameter_config = parameter_config
        self.table_logger = table_logger
        self.event_publisher = event_publisher
        self.rules_list = [OneTableRule()]
        
    def execute(self, message: OrquestradorMessageAdapter):
        # Registrar Log
        self._save_message_in_table_logger(message)
        # Recuperar Configuração
        configs: List[Event] = self._recovery_config_off_message(message)
        # Agregar evento e calcular eventos para emitir
        events_to_publish: EventLayoutAdapter = self._apply_rules_to_aggregate_event(message, configs)
        # Publicar Evento
        self._publish_events(events_to_publish)

    def _save_message_in_table_logger(self, message: OrquestradorMessageAdapter):
        stream_name: str = self.table_logger.create_stream(message['TableName'])

        self.table_logger.save_log(stream_name= stream_name, event=message)

    def _recovery_config_off_message(self, message: OrquestradorMessageAdapter) -> List[Event]:
        # Agregar Evento
        configs_all: List[Event] = self.parameter_config.get_all_config()
        #filtrar todas as configs que tem a tabela da mensagem
        configs_filtered: List[Event] = [event for event in configs_all
                                        if message['TableName'] in
                                        [table.name for table in event.tables]]
        return configs_filtered

    def _apply_rules_to_aggregate_event(self, message: OrquestradorMessageAdapter, configs: List[Event]) -> EventLayoutAdapter:
        events_to_publish: EventLayoutAdapter = {}
        for rule in self.rules_list:
            events_to_publish.update(rule.apply_rule(message, configs))
        return events_to_publish

    def _publish_events(self, events: EventLayoutAdapter):
        for event in events:
            self.event_publisher.publish_event(event)