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


def test_is_column_present_with_valid_column():
	assert Settings.is_column_present("url") == "url"


def test_is_column_present_case_sensitivity():
	assert Settings.is_column_present("URL") is None


def test_is_column_present_with_invalid_column(capsys):
	invalid_column_name = "invalid_column"
	expected_output = (
		f"Некорректное имя столбца => {invalid_column_name}. "
		f"Введите один из доступных => ['number', 'key', 'url', 'last_date_time', 'included']\n"
	)
	assert Settings.is_column_present(invalid_column_name) is None
	assert capsys.readouterr().out == expected_output


def test__check_table_code_with_valid_code():
	# noinspection PyUnresolvedReferences
	assert Settings._Settings__check_table_code("BL") == "BL"  # noqa: SLF001


def test__check_table_code_case_sensitivity():
	# noinspection PyUnresolvedReferences
	assert Settings._Settings__check_table_code("bl") is None  # noqa: SLF001


def test__check_table_code_with_invalid_code(capsys):
	invalid_table_code = "invalid_column"
	expected_output = (
		f"Некорректный код => {invalid_table_code}. "
		f"Введите один из доступных => ['ST', 'BL', 'VL']\n"
	)
	# noinspection PyUnresolvedReferences
	assert Settings._Settings__check_table_code(invalid_table_code) is None  # noqa: SLF001
	assert capsys.readouterr().out == expected_output
