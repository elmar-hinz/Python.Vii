from collections import defaultdict

register = defaultdict(list)

def signal(id, subject):
    for observer in register[id]:
        observer.receive(id, subject)

def slot(id, subject):
    register[id].append(subject)


