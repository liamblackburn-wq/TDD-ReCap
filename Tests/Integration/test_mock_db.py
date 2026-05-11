from db import DatabaseService
import pytest
import sqlite3
from unittest.mock import Mock

def mock_sql_connection(rows_to_return):
    con = Mock()
    cursor = Mock()

    cursor.fetchall.return_value = rows_to_return
    cursor.execute.return_value = cursor
    con.cursor.return_value = cursor

    return con

@pytest.mark.parametrize("duty_id_list, expected_result", (
        ([1, 2, 3], ["Duty 1", "Duty 2", "Duty 3"]),
        ([1, 3], ["Duty 1", "Duty 3"])
))
def test_get_duty_descriptions_returns_descriptions(duty_id_list, expected_result):
    rows_to_return = [(description,) for description in expected_result]
    mock_con = mock_sql_connection(rows_to_return)

    db = DatabaseService(mock_con)
    actual_result = db.get_duty_descriptions(duty_id_list)

    assert actual_result == expected_result

