
def up(position, count):
    return (position[0] - count, position[1])

def down(position, count):
    return (position[0] + count, position[1])

def left(position, count):
    return (position[0], position[1] - count)

def right(position, count):
    return (position[0], position[1] + count)


