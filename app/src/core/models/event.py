from dataclasses import dataclass
# from app.src.core.interface.aggregate_rules import IAggregationRule
from .process import Process
from .table import Table

@dataclass
class Event:
    id: int
    rule_type: str
    name: str
    processes: list[Process]
    tables: list[Table]

    ## This method is called when the object is created
    def __post_init__(self):
        self.validate()
        # self.validate_rule_type_value()

    # Validate the object
    def validate(self):
        if not self.id or self.id == '':
            raise ValueError('Id is required')
        if not self.rule_type or self.rule_type == '':
            raise ValueError('Rule Type is required')
        if not self.name or self.name == '':
            raise ValueError('Name is required')
        if not self.processes or self.processes == '':
            raise ValueError('Process is required')
        if not self.tables or self.tables == '':
            raise ValueError('Table is required')
        
    # # Validate the origem value
    # def validate_rule_type_value(self):

    #     values = [str(rule.__name__) for rule in IAggregationRule.__subclasses__()]

    #     if self.rule_type not in values:
    #         raise ValueError(f'Rules must be one of the following: {values}')
        