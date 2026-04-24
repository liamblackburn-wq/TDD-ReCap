from db import DatabaseService
import pytest
import sqlite3
from unittest.mock import Mock

def mock_sql_connection(rows_to_return):
    con = Mock()
    cursor = Mock()
    result_set = Mock()
    result_set.fetchall.return_value = rows_to_return

    cursor.execute.return_value = result_set
    con.cursor.return_value = cursor

@pytest.mark.parametrize("duty_id_list, expected_result", (
        ([1, 2, 3], ["Duty 1", "Duty 2", "Duty 3"]),
        ([1, 3], ["Duty 1", "Duty 3"])
))
def xtest_get_duty_descriptions_returns_descriptions(duty_id_list, expected_result):
    # rows_to_return =
    # iterate over duty_id list and result, zip together.
    # python zip function maybe?

    db = DatabaseService(mock_sql_connection(rows_to_return))

    actual_result = db.get_duty_descriptions(duty_id_list)

    assert actual_result == expected_result

