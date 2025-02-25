import data


def test_database_connection_parameters():
	"""Do database connection parameters correctly retrieve from environment variables?"""
	expected_connection_parameters = {
		"host": "test_localhost",
		"port": "5439",
		"database": "test_bot_db",
		"user": "test_postgres",
		"password": "p7As5s",
	}

	actual_database_name = data.Settings.get_name_database()
	assert actual_database_name == expected_connection_parameters["database"]

	actual_connection_parameters = data.Settings.get_db_connection_parameters()
	assert actual_connection_parameters == expected_connection_parameters

	del expected_connection_parameters["database"]
	actual_connection_parameters_without_database = data.Settings.get_db_connection_parameters(
		without_database=True
	)
	assert actual_connection_parameters_without_database == expected_connection_parameters
