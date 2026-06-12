from duties import Duty

def test_duty_features():
    test_duty = Duty("Duty 1", "Test Description")
    assert test_duty.name ==  "Duty 1"
    assert test_duty.description == "Test Description"

def test_duties_with_same_name_are_equal():
    duty_1 = Duty("Duty 5", "CI/CD")
    duty_2 = Duty("Duty 5", "CI/CD")

    assert duty_1 == duty_2
