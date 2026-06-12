from duties import Duty

def test_duty_features():
    test_duty = Duty("Duty 1", "Test Description")
    assert test_duty.name ==  "Duty 1"
    assert test_duty.description == "Test Description"

