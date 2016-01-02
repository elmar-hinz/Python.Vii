from collections import defaultdict

register = defaultdict(list)

def signal(signal, sender, *args):
    for observer in register[signal]:
        observer.receive(signal, sender, *args)

def slot(signal, receiver):
    register[signal].append(receiver)

"""
TODO: unslot

There will be a lot of cursors listening, one
for each window/buffer combination. When buffers
or windows are closed they should be removed,
else the garbage collection can't do its job.

Receivers as keys of a list will be faster.
"""


