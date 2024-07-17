from app.src.dataprovider.services.file_parameter_config import FileParameterConfig
from app.src.core.models import Event, Table, Process
from typing import Dict
import yaml


## Test Official Config
def test_official_yaml_config():
    file_parameter_config = FileParameterConfig("app/config.yml")
    events = file_parameter_config.get_all_config()
    assert isinstance(events, list)
    for event in events:
        assert type(event) == Event
        assert isinstance(event.id, int)
        assert isinstance(event.rule_type, str)
        assert isinstance(event.name, str)
        assert isinstance(event.processes, list)
        for process in event.processes:
            assert type(process) == Process
            assert isinstance(process.name, str)
            assert isinstance(process.description, str)
        assert isinstance(event.tables, list)
        for table in event.tables:
            assert type(table) == Table
            assert isinstance(table.name, str)
            assert isinstance(table.database, str)
            assert isinstance(table.description, str)
            assert isinstance(table.origin, str)


def test_official_yaml_config_table_not_have_duplicate_name():
    with open("app/config.yml", "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    for name, table in data["tables"].items():
        assert name == table["name"]


def test_official_yaml_config_process_not_have_duplicate_name():
    with open("app/config.yml", "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    for name, process in data["processes"].items():
        assert name == process["name"]


def test_official_yaml_config_there_is_no_duplicate_table_event_config():
    with open("app/config.yml", "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    seen = set()
    for d in data["events"]:
        if "tables" in d:
            print(d['tables'])
            table_tuple = tuple(tuple(sorted(item.items())) if isinstance(item, dict) else item for item in d['tables'])
            if table_tuple in seen:
                assert False, f"Tabelas para agregar em evento estão em duplicidades em mais de uma carga: {d['name']}"
            seen.add(table_tuple)
    assert True


## Test Functions
def test_safe_load_yaml_config():
    file_parameter_config = FileParameterConfig("tests/fixtures/mock_config_succeeded.yml")
    events = file_parameter_config.get_all_config()
    assert len(events) == 3
    assert events[0].id == 1
    assert events[0].name == "EventA"
    assert events[0].processes[0].name == "Carga1"
    assert events[0].processes[1].name == "Carga4"
    assert events[0].tables[0].name == "TabelaA"
    assert events[0].tables[0].description == "Tabela contendo informações da tabela A"
    assert events[0].tables[0].origin == "ACL"
    assert events[1].id == 2
    assert events[1].name == "EventAandB"
    assert events[1].processes[0].name == "Carga2"
    assert events[1].tables[0].name == "TabelaA"
    assert events[1].tables[0].description == "Tabela contendo informações da tabela A"
    assert events[1].tables[0].origin == "ACL"
    assert events[1].tables[1].name == "TabelaB"
    assert events[1].tables[1].description == "Tabela contendo informações da tabela B"
    assert events[1].tables[1].origin == "DATAMESH"
    assert events[2].id == 3
    assert events[2].name == "EventB"
    assert events[2].processes[0].name == "Carga3"
    assert events[2].tables[0].name == "TabelaB"
    assert events[2].tables[0].description == "Tabela contendo informações da tabela B"
    assert events[2].tables[0].origin == "DATAMESH"

def test_file_config_not_found():
    file_parameter_config = FileParameterConfig("tests/fixtures/not_found_config.yml")
    try:
        file_parameter_config.get_all_config()
        assert False
    except Exception as e:
        assert isinstance(e, FileNotFoundError)


def test_error_mapping_event_config():
    file_parameter_config = FileParameterConfig("tests/fixtures/mock_config_failed.yml")
    try:
        file_parameter_config.get_all_config()
        assert False
    except Exception as e:
        assert isinstance(e, ValueError)
        assert (
            str(e)
            == "Error loading config: Error mapping event config: Table.__init__() missing 1 required positional argument: 'description'"
        )


def test_mapping_missing_process_description():
    file_parameter_config = FileParameterConfig("")
    config_one_event_mock: Dict = {
        "id": 1,
        "name": "EventA",
        "processes": [
            {"name": "Carga1"},
            {"name": "Carga4", "description": "Processo de gerenciamento de Carga4"},
        ],
        "tables": [{"name": "TabelaA", "description": "Tabela contendo informações da tabela A", "origin": "ACL"}],
    }
    try:
        file_parameter_config._mapping_event(config_one_event_mock)
        assert False
    except Exception as e:
        assert isinstance(e, ValueError)
        assert (
            str(e)
            == "Error mapping event config: Process.__init__() missing 1 required positional argument: 'description'"
        )


def test_mapping_missing_process():
    file_parameter_config = FileParameterConfig("")
    config_one_event_mock: Dict = {
        "id": 1,
        "name": "EventA",
        "rule_type": "SAME PARTITION",
        "processes": [],
        "tables": [{"name": "TabelaA", "database": "DatabaseA", "description": "Tabela contendo informações da tabela A", "origin": "ACL"}],
    }
    try:
        file_parameter_config._mapping_event(config_one_event_mock)
        assert False
    except Exception as e:
        assert isinstance(e, ValueError)
        assert str(e) == "Error mapping event config: Process is required"


## testar chaves duplicadas depois
