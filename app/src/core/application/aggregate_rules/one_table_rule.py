from typing import List
from app.src.core.models import Event
from app.src.core.interface.aggregate_rules.aggregate_rule import IAggregationRule
from app.src.core.models.types.orquestrador_message_adapter import OrquestradorMessageAdapter
from app.src.core.models.types.event_layout_adapter import EventLayoutAdapter


class OneTableRule(IAggregationRule):

    def apply_rule(self, event_data: OrquestradorMessageAdapter, config_list: List[Event]) -> EventLayoutAdapter:

        data: EventLayoutAdapter = {}
        for config in config_list:
            if config.rule_type == "One Table" and event_data["TableName"] in [table.name for table in config.tables]:
                data.update(
                    {
                        "Source": f"{config.tables[0].name}",
                        "DetailType": "Orquestrador One Table Rule",
                        "Detail": {"Config": config.to_dict(), "Message": event_data},
                    }
                )

        return data
