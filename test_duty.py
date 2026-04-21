class Duty:
    def __init__(self, name, description):
        self.name = name
        self._description = description
    
    def equals(self, duty2):
        return self.name == duty2.name
    
    def description(self):
        return self._description


duty1 = Duty("duty1", "Script and code")
duty2 = Duty("duty2", "Initiate and facilitate")

def test_duty_returns_name():
    assert isinstance(duty1, Duty)

def test_duty1_and_duty2_are_different():
    
    assert duty1.equals(duty2) is False

def test_duties_has_description():
    assert "Script and code" in duty1.description() 
    assert "Initiate and facilitate" in duty2.description()
