from duties import Duty

def test_duty_name():
    test_duty = Duty("Duty 1")
    assert test_duty.name ==  "Duty 1"

def test_duty_description():
    test_duty = Duty("Duty 1", "Test Description")
    test_duty.description = "Test Description"
    assert test_duty.description == "Test Description"
