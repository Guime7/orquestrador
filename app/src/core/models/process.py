from dataclasses import dataclass
import re

@dataclass
class Process:
    name: str
    description: str
    frequency_expected_to_run: str = None
    time_cut_report_not_executed: str = None

    ## This method is called when the object is created
    def __post_init__(self):
        self.validate()
        self.validate_frequency_expected_to_run()
        self.validate_time_cut_report_not_executed()

    # Validate the object
    def validate(self):
        if not self.name or self.name == '':
            raise ValueError('Name is required')
        if not self.description or self.description == '':
            raise ValueError('Description is required')
    
    def validate_frequency_expected_to_run(self):
        values = ['Diária']
        if self.frequency_expected_to_run not in values and self.frequency_expected_to_run is not None:
            raise ValueError(f'Frequency Expected To Run must be one of the following: {values}')
        
 
    def validate_time_cut_report_not_executed(self):
        pattern = r'^\d{2}:\d{2}$'
        if self.time_cut_report_not_executed is not None and not re.match(pattern, self.time_cut_report_not_executed):
            raise ValueError('Time Cut Report Not Executed must be in the format 00:00')
        