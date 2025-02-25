from importlib import reload

import pytest

import data


@pytest.fixture
def mock_database_envs(monkeypatch):
	"""Mock environment variables for database connection parameters for testing."""
	monkeypatch.setenv("DB_HOST", "test_localhost")
	monkeypatch.setenv("DB_PORT", "5439")
	monkeypatch.setenv("DB_NAME", "test_bot_db")
	monkeypatch.setenv("DB_USER", "test_postgres")
	monkeypatch.setenv("DB_PASSWORD", "p7As5s")

	reload(data)


def test_database_connection_parameters(mock_database_envs):
	"""Do database connection parameters correctly retrieve from environment variables?"""
	expected_parameters = {
		"host": "test_localhost",
		"port": "5439",
		"database": "test_bot_db",
		"user": "test_postgres",
		"password": "p7As5s",
	}
	actual_database_name = data.Settings.get_name_database()
	assert actual_database_name == expected_parameters["database"]
	actual_params = data.Settings.get_db_connection_parameters()
	assert actual_params == expected_parameters
	del expected_parameters["database"]
	actual_params_without_database = data.Settings.get_db_connection_parameters(
		without_database=True
	)
	assert actual_params_without_database == expected_parameters


@pytest.mark.parametrize(
	("method_to_test", "expected"),
	[
		("get_name_database", "test_bot_db"),
		(
			"get_db_connection_parameters",
			{
				"host": "test_localhost",
				"port": "5439",
				"database": "test_bot_db",
				"user": "test_postgres",
				"password": "p7As5s",
			},
		),
	],
)
def test_settings_methods(mock_database_envs, method_to_test, expected):
	"""Do database connection parameters correctly retrieve from environment variables?"""
	result = getattr(data.Settings, method_to_test)()
	assert result == expected
