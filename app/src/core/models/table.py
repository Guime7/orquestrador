from dataclasses import dataclass

@dataclass
class Table:
    name: str
    database: str
    description: str
    origin: str
    frequency_expected_to_receive: str = None

    ## This method is called when the object is created
    def __post_init__(self):
        self.validate()
        self.validate_origin_value()
        self.validate_frequency_expected_to_receive()

    # Validate the object
    def validate(self):
        if not self.name or self.name == '':
            raise ValueError('Name is required')
        if not self.database or self.database == '':
            raise ValueError('Database is required')
        if not self.description or self.description == '':
            raise ValueError('Description is required')
        if not self.origin or self.origin == '':
            raise ValueError('Origin is required')
    
    # Validate the origem value
    def validate_origin_value(self):
        values = ['ACL', 'DATAMESH', "LIFTSHIFT", "API", "KAFKA"]
        if self.origin not in values:
            raise ValueError(f'Origem must be one of the following: {values}')
        
    def validate_frequency_expected_to_receive(self):
        values = ['Diária']
        if self.frequency_expected_to_receive not in values and self.frequency_expected_to_receive is not None:
            raise ValueError(f'Frequency Expected To Receive must be one of the following: {values}')