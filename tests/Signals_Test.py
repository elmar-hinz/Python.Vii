import vii.Signals as signals

class ObserverCorrectlyCalled1(Exception): pass
class ObserverCorrectlyCalled2(Exception): pass

class Sender(): pass

sender1 = Sender()
sender2 = Sender()

class Receiver():
    def receive(self, signal, sender, **kwargs):
        if signal == "sig" and sender == sender1:
            raise ObserverCorrectlyCalled1
        if(signal == "sig" and sender == sender2
            and kwargs == {'key1':1, 'key2':2}
            ):
            raise ObserverCorrectlyCalled2

receiver1 = Receiver()
receiver2 = Receiver()

def test_registerIsUniqe():
    import vii.Signals as signals
    signals.register["a"].append(1)
    assert 1 in signals.register["a"]
    import vii.Signals as signals
    assert 1 in signals.register["a"]

def test_slotRegistersObjects():
    signals.slot("b", receiver1)
    signals.slot("b", receiver2)
    assert receiver1 in signals.register["b"]
    assert receiver2 in signals.register["b"]

def test_signalCallsAllObservers():
    signals.slot("sig", receiver1)
    signals.slot("sig", receiver2)

    seen = False
    try: signals.signal("sig", sender1)
    except ObserverCorrectlyCalled1: seen = True
    assert seen

    seen = False
    try: signals.signal("sig", sender2, key1=1, key2=2)
    except ObserverCorrectlyCalled2: seen = True
    assert seen



