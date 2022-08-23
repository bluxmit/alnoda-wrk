import pytest
from pathlib import Path
from alnoda_wrk.conf_parser import *
import yaml
import os

def read_test_conf(conf_file):
    dirpath = os.path.dirname(Path(__file__))
    with open(os.path.join(dirpath, 'workspace-yaml', conf_file), 'r') as stream:
        wrk_params = yaml.safe_load(stream)
    return wrk_params

def test_main_keys_correct():
    """ Example of the proper workspace.yaml
    Should check all main keys are present
    """
    wrk_params = read_test_conf('workspace-correct.yaml')
    assert validate_main_required_keys_present(wrk_params)

def test_missing_name():
    """ Example of the workspace.yaml with missing name
    Should check proper exception is raised
    """
    wrk_params = read_test_conf('workspace-missing-name.yaml')
    with pytest.raises(Exception) as e:
        validate_main_required_keys_present(wrk_params)
    assert REQUIRED_KEYS["name"] in str(e.value) 
    assert e.type == Exception

def test_missing_descr_val():
    """ Example of the workspace.yaml with missing value for description
    Should check proper exception is raised
    """
    wrk_params = read_test_conf('workspace-no-descr-val.yaml')
    with pytest.raises(Exception) as e:
        validate_main_required_keys_present(wrk_params)
    assert REQUIRED_KEYS["description"] in str(e.value) 
    assert e.type == Exception

def test_valid_schema():
    """ Example of the proper workspace.yaml.
    Should check schema validation is OK
    """
    wrk_params = read_test_conf('workspace-correct.yaml')
    assert validate_schema(wrk_params)

def test_valid_schema():
    """ Example of the proper workspace.yaml with no styles
    Styles are optionsl
    Should check schema validation is OK
    """
    wrk_params = read_test_conf('workspace-correct.yaml')
    assert validate_schema(wrk_params)

def test_invalid_schema_miss_descr():
    """ Example of the improper workspace yaml
    Should check schema validation is not OK 
    Required field missing value
    """
    wrk_params = read_test_conf('workspace-no-descr-val.yaml')
    with pytest.raises(Exception) as e:
        assert validate_schema(wrk_params)
    assert "{'description': ['null value not allowed']}" in str(e.value)
    assert e.type == Exception

def test_invalid_schema_opt_field_miss_val():
    """ Example of the improper workspace yaml
    Should check schema validation is not OK:
    logo is optional, but if it is there, the value must be present 
    """
    wrk_params = read_test_conf('workspace-opt-field-miss-val.yaml')
    with pytest.raises(Exception) as e:
        assert validate_schema(wrk_params)
    assert "{'logo': ['null value not allowed']}" in str(e.value)
    assert e.type == Exception

def test_invalid_schema_req_field_in_opt_nest_miss_val():
    """ Example of the improper workspace yaml
    Should check schema validation is not OK:
    title is required in tools for home page
    """
    wrk_params = read_test_conf('workspace-miss-nest-field.yaml')
    with pytest.raises(Exception) as e:
        assert validate_schema(wrk_params)
    assert e.type == Exception

def test_invalid_schema_incorrect_field_type():
    """ Example of the improper workspace yaml
    Should check schema validation is not OK:
    port should be number
    """
    wrk_params = read_test_conf('workspace-incorrect-type.yaml')
    with pytest.raises(Exception) as e:
        assert validate_schema(wrk_params)
    assert e.type == Exception

def test_invalid_schema_incorrect_sructure():
    """ Example of the improper workspace yaml
    Should check schema validation is not OK:
    incorrect nested dict structure
    """
    wrk_params = read_test_conf('workspace-incorrect-struct.yaml')
    with pytest.raises(Exception) as e:
        assert validate_schema(wrk_params)
    assert e.type == Exception

