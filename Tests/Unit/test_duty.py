import pytest

from duties import Duty

def test_duty_features():
    test_duty = Duty("Duty 1", "Test Description")
    assert test_duty.name ==  "Duty 1"
    assert test_duty.description == "Test Description"

def test_duties_with_same_features_are_equal():
    duty_1 = Duty("Duty 5", "CI/CD")
    duty_2 = Duty("Duty 5", "CI/CD")

    assert duty_1 == duty_2

def test_duties_with_different_features_are_not_equal():
    duty_1 = Duty("Duty 5", "CI/CD")
    duty_2 = Duty("Duty 5", "Different Description")
    duty_3 = Duty("Duty 5", "CI/CD")
    duty_4 = Duty("Duty 6", "CI/CD")

    assert duty_1 != duty_2
    assert duty_3 != duty_4

def test_invalid_duty_raises_error():
    with pytest.raises(ValueError) as exc_info:
        Duty("TEAPOT", "Test Description")
