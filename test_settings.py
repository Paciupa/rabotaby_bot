import pytest

from data import Settings


@pytest.mark.parametrize(
	("method_to_test", "args", "expected_result"),
	[
		("get_database_name", (), "test_bot_db"),
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


@pytest.mark.parametrize(
	("method_to_test", "expected_output"),
	[
		(
			"is_column_present",
			(
				"Некорректное имя столбца => {}. Введите один из доступных "
				"=> ('number', 'key', 'url', 'last_date_time', 'included')\n"
			),
		),
		(
			"_Settings__check_table_code",
			"Некорректный код => {}. Введите один из доступных => ['ST', 'BL', 'VL']\n",
		),
	],
)
def test_settings_methods_stdout(capsys, method_to_test, expected_output):
	assert getattr(Settings, method_to_test)("invalid_argument") is None
	assert capsys.readouterr().out == expected_output.format("invalid_argument")


@pytest.mark.parametrize(
	("method_to_test", "arg"),
	[
		("get_table_name_by_code", "bl"),
		("get_table_name_by_code", "invalid_table_code"),
		("get_query", "vl"),
		("get_query", "invalid_table_code"),
	],
)
def test_settings_methods_exception(method_to_test, arg):
	with pytest.raises(KeyError, match="None"):
		_ = getattr(Settings, method_to_test)(arg)


def test__get_setting_for_parameter_with_valid_table_code():
	expected_output = (
		"number INTEGER NOT NULL",
		"key TEXT NOT NULL",
		"url TEXT NOT NULL",
		"included BOOLEAN NOT NULL",
	)
	# noinspection PyUnresolvedReferences
	assert tuple(Settings._Settings__get_setting_for_parameter("BL")) == expected_output  # noqa: SLF001


@pytest.mark.parametrize("arg", ["bl", "invalid_table_code"])
def test__get_setting_for_parameter_exception(arg):
	with pytest.raises(KeyError, match="None"):
		# noinspection PyUnresolvedReferences
		_ = tuple(Settings._Settings__get_setting_for_parameter(arg))  # noqa: SLF001
