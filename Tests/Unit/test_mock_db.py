from db import DatabaseService
import pytest
from unittest.mock import Mock

duty_1_description = ("Script and code in at least one general purpose language and at least one domain-specific "
                      "language to orchestrate infrastructure, follow test driven development "
                      "and ensure appropriate test coverage.")

duty_3_description = "Engage in productive pair/mob programming to underpin the practice of peer review."

def mock_sql_connection(rows_to_return):
    con = Mock()
    cursor = Mock()

    cursor.fetchall.return_value = rows_to_return
    cursor.execute.return_value = cursor
    con.cursor.return_value = cursor

    return con

@pytest.mark.parametrize("duty_id_list, expected_result", (
        ([1], [{"Duty": "Duty 1", "Description": duty_1_description}]),
        ([1, 3], [
            {"Duty": "Duty 1", "Description": duty_1_description},
            {"Duty": "Duty 3", "Description": duty_3_description}
        ]),
))
def test_get_duty_descriptions_returns_descriptions(duty_id_list, expected_result):
    rows_to_return = [(item["Duty"], item["Description"]) for item in expected_result]
    mock_con = mock_sql_connection(rows_to_return)

    db = DatabaseService(mock_con)
    actual_result = db.get_duty_descriptions(duty_id_list)

    assert actual_result == expected_result


def test_save_duties_executes_correct_query():
    mock_con = mock_sql_connection([])
    db = DatabaseService(mock_con)

    db.save_duties([1, 2])

    assert mock_con.cursor().executemany.called

def test_get_saved_duties_executes_correct_query():
    mock_con = mock_sql_connection([])
    db = DatabaseService(mock_con)
    db.get_saved_duties()
    assert mock_con.cursor().execute.called

def test_remove_saved_duty_executes_correct_query():
    mock_con = mock_sql_connection([])
    db = DatabaseService(mock_con)
    db.remove_saved_duty([1, 2])
    assert mock_con.cursor().execute.called