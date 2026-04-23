import db
from db import Duties

duty1 = Duties("duty1", "Script and code")
duty2 = Duties("duty2", "Initiate and facilitate")

def fake_call():
    return [{

    }]

def test_db_is_called_successfully(mocker):

    mock_data = [{
        
    }]
    mock_response = mocker.Mock()
    mock_response.json.return_value = mock_data

    mocker.patch("db.call_database", return_value=mock_response)

    actual_result = db.call_database()

    db.call_database.assert_called_once()


def test_duty_returns_name():
    assert isinstance(duty1, Duties)

def test_duty1_and_duty2_are_different():    
    assert duty1.equals(duty2) is False

def test_duties_has_description():
    assert "Script and code" in duty1.description() 
    assert "Initiate and facilitate" in duty2.description()


    