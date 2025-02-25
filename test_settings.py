import pytest

from data import Settings


@pytest.mark.parametrize(
	("method_to_test", "args", "expected_result"),
	[
		("get_name_database", (), "test_bot_db"),
		(
			"get_db_connection_parameters",
			(),
			{
				"host": "test_localhost",
				"port": "5439",
				"database": "test_bot_db",
				"user": "test_postgres",
				"password": "p7As5s",
			},
		),
		(
			"get_db_connection_parameters",
			(True,),
			{
				"host": "test_localhost",
				"port": "5439",
				"user": "test_postgres",
				"password": "p7As5s",
			},
		),
	],
	ids=[
		"get_database_name",
		"get_database_connection_parameters_full",
		"get_database_connection_parameters_without_name",
	],
)
def test_settings_methods(method_to_test, args, expected_result):
	result = getattr(Settings, method_to_test)(*args)
	assert result == expected_result
