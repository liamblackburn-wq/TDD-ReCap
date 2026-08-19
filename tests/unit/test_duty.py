from unittest.mock import patch

import pytest
import uuid

from peewee import DatabaseError

from src.models import Duty


def test_duty_features():
    test_duty = Duty(id=uuid.uuid4(), name="Duty 1", description="Test Description")
    assert test_duty.name == "Duty 1"
    assert test_duty.description == "Test Description"


def test_duties_with_same_features_are_equal():
    duty_1 = Duty(id=uuid.uuid4(), name="Duty 5", description="CI/CD")
    duty_2 = Duty(id=uuid.uuid4(), name="Duty 5", description="CI/CD")

    assert duty_1 == duty_2


def test_duties_with_different_features_are_not_equal():
    duty_1 = Duty(id=uuid.uuid4(), name="Duty 5", description="CI/CD")
    duty_2 = Duty(id=uuid.uuid4(), name="Duty 5", description="Different Description")

    duty_3 = Duty(id=uuid.uuid4(), name="Duty 5", description="CI/CD")
    duty_4 = Duty(id=uuid.uuid4(), name="Duty 6", description="CI/CD")

    assert duty_1 != duty_2
    assert duty_3 != duty_4


def test_invalid_duty_raises_error():
    error_message = "Duty name must start with 'Duty' followed by a number."
    invalid_duty = Duty(id=uuid.uuid4(), name="WRONG", description="WRONG")

    with pytest.raises(ValueError, match=error_message):
        invalid_duty.validate()


def test_duty_equality_dunder_method_true_for_identical_duty_name():
    duty_a = Duty(name="Test_duty")
    duty_b = Duty(name="Test_duty")

    assert duty_a == duty_b


def test_duty_equality_dunder_method_true_for_unidentical_duty_name():
    duty_a = Duty(name="Duty_a")
    duty_b = Duty(name="Duty_b")

    assert duty_a != duty_b


def test_duty_equality_dunder_method_true_for_different_object_types():
    duty = Duty(name="Test")

    assert duty != "Test"
