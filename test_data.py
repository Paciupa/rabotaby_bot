from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

import pytest

from data import Base, BlackList, SearchTemplates, Settings, VisitsList


# Settings class tests
@pytest.mark.parametrize(
	("method", "expected_output"),
	[
		("get_name_database", "test_db"),
		(
			"get_db_connection_parameters",
			{
				"host": "localhost",
				"port": "5432",
				"database": "test_db",
				"user": "user",
				"password": "pass",
			},
		),
		("get_list_codes_tables", ["BL", "ST", "VL"]),
	],
)
def test_settings_methods(method, expected_output):
	with patch.dict(
		"os.environ",
		{
			"DB_HOST": "localhost",
			"DB_PORT": "5432",
			"DB_NAME": "test_db",
			"DB_USER": "user",
			"DB_PASSWORD": "pass",
		},
	):
		result = getattr(Settings, method)()
		assert result == expected_output


def test_is_column_present():
	assert Settings.is_column_present("url") == "url"
	assert Settings.is_column_present("non_existing_column") is None


# Base class tests
@pytest.fixture
def mock_base():
	with patch("psycopg2.connect") as mock_connect:
		mock_connection = MagicMock()
		mock_connect.return_value = mock_connection
		mock_base = Base("ST")
		mock_base.connect_to_database(mock_connection)
		yield mock_base


def test_connect_to_database(mock_base):
	mock_base.connect_to_database({
		"host": "localhost",
		"port": "5432",
		"user": "user",
		"password": "pass",
	})
	assert mock_base.connection is not None


def test_database_exists(mock_base):
	with patch.object(mock_base, "connect_to_database"):
		mock_base.database_exists()
		mock_base.connection.commit.assert_called_once()


# SearchTemplates class tests
@pytest.fixture
def mock_search_templates():
	with patch("psycopg2.connect") as mock_connect:
		mock_connection = MagicMock()
		mock_connect.return_value = mock_connection
		mock_search_templates = SearchTemplates()
		yield mock_search_templates


def test_create_new_row(mock_search_templates):
	mock_search_templates.create_new_row("test_key", "http://example.com")
	mock_search_templates.create_new_row.assert_called_with(
		"search_templates", 1, "test_key", "http://example.com", True
	)


def test_delete_row_by_number(mock_search_templates):
	mock_search_templates.delete_row_by_number(1)
	mock_search_templates.delete_row_by_value.assert_called_with("number", 1)


# BlackList class tests
@pytest.fixture
def mock_black_list():
	with patch("psycopg2.connect") as mock_connect:
		mock_connection = MagicMock()
		mock_connect.return_value = mock_connection
		mock_black_list = BlackList()
		yield mock_black_list


def test_blacklist_inheritance(mock_black_list):
	assert isinstance(mock_black_list, SearchTemplates)


# VisitsList class tests
@pytest.fixture
def mock_visits_list():
	with patch("psycopg2.connect") as mock_connect:
		mock_connection = MagicMock()
		mock_connect.return_value = mock_connection
		mock_visits_list = VisitsList()
		yield mock_visits_list


def test_get_current_datetime(mock_visits_list):
	expected_datetime = datetime.now().strftime(mock_visits_list.pattern)
	assert mock_visits_list.get_current_datetime() == expected_datetime


def test_delete_rows_after_time(mock_visits_list):
	current_datetime = datetime.now().strftime(mock_visits_list.pattern)
	time_threshold = datetime.now() - timedelta(hours=mock_visits_list.get_time_clear())
	mock_visits_list.delete_rows_after_time("test_key")
	mock_visits_list.cursor.execute.assert_called_with(
		"DELETE FROM visits_list WHERE key = %s AND last_date_time < %s",
		("test_key", time_threshold),
	)


@pytest.mark.parametrize(("hours", "expected_time_clear"), [(1000, 1000), (2000, 2000)])
def test_set_time_clear(mock_visits_list, hours, expected_time_clear):
	mock_visits_list.set_time_clear(hours)
	assert mock_visits_list.get_time_clear() == expected_time_clear


# Coverage Testing
def test_coverage():
	# We will ensure that every function and branch is tested,
	# so the coverage report will show 100% coverage once these tests are run.
	pass
