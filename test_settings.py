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
		("get_list_codes_tables", (), ["ST", "BL", "VL"]),
		("is_column_present", ("url",), "url"),
		("_Settings__check_table_code", ("BL",), "BL"),
		("get_table_name_by_code", ("BL",), "black_list"),
		(
			"get_query",
			("VL",),
			(
				"CREATE TABLE IF NOT EXISTS visits_list "
				"(last_date_time TIMESTAMP NOT NULL, key TEXT NOT NULL, url TEXT NOT NULL)"
			),
		),
	],
	ids=[
		"get_database_name",
		"get_database_connection_parameters_full",
		"get_database_connection_parameters_without_name",
		"get_list_codes_tables",
		"is_column_present_with_valid_column",
		"__check_table_code_with_valid_code",
		"get_table_name_by_code_with_valid_table_code",
		"get_query_with_valid_table_code",
	],
)
def test_settings_methods(method_to_test, args, expected_result):
	result = getattr(Settings, method_to_test)(*args)
	assert result == expected_result


@pytest.mark.parametrize(
	("method_to_test", "arg"), [("is_column_present", "URL"), ("_Settings__check_table_code", "bl")]
)
def test_settings_methods_case_sensitivity(method_to_test, arg):
	assert getattr(Settings, method_to_test)(arg) is None
