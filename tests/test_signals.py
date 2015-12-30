import vii.signals as signals

class ObserverCorrectlyCalled1(Exception): pass
class ObserverCorrectlyCalled2(Exception): pass

class Observer():
    def receive(self, id, subject):
        if id == "o" and subject == "message1":
            raise ObserverCorrectlyCalled1
        if id == "o" and subject == "message2":
            raise ObserverCorrectlyCalled2

def test_registerIsUniqe():
    import vii.signals as signals
    signals.register["a"].append(1)
    assert 1 in signals.register["a"]
    import vii.signals as signals
    assert 1 in signals.register["a"]

def test_slotRegistersObjects():
    signals.slot("b", "c")
    signals.slot("b", "d")
    assert "c" in signals.register["b"]
    assert "d" in signals.register["b"]

def test_signalCallsAllObservers():
    signals.slot("o", Observer())
    signals.slot("o", Observer())

    seen = False
    try: signals.signal("o", "message1")
    except ObserverCorrectlyCalled1: seen = True
    assert seen

    seen = False
    try: signals.signal("o", "message2")
    except ObserverCorrectlyCalled2: seen = True
    assert seen



