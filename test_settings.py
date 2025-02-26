import pytest

from data import Settings

# Test database connection parameters


@pytest.fixture
def expected_database_connection_parameters():
	return {
		"host": "test_localhost",
		"port": "5439",
		"database": "test_bot_db",
		"user": "test_postgres",
		"password": "p7As5s",
	}


def test_get_database_name(expected_database_connection_parameters):
	actual_database_name = Settings.get_name_database()
	assert actual_database_name == expected_database_connection_parameters["database"]


def test_get_database_connection_parameters_full(expected_database_connection_parameters):
	actual_connection_parameters = Settings.get_db_connection_parameters()
	assert actual_connection_parameters == expected_database_connection_parameters


def test_get_database_connection_parameters_without_name(expected_database_connection_parameters):
	del expected_database_connection_parameters["database"]
	actual_connection_parameters_without_database = Settings.get_db_connection_parameters(
		without_database=True
	)
	assert actual_connection_parameters_without_database == expected_database_connection_parameters


def test_get_list_codes_tables():
	expected_code_tables = ["ST", "BL", "VL"]
	actual_code_tables = Settings.get_list_codes_tables()
	assert sorted(actual_code_tables) == sorted(expected_code_tables)
