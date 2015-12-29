class Cursor:

    buffer = None
    x, y = 0, 0

    def moveVertical(self, offset):
        y = self.y + offset
        height = self.buffer.length()
        if y < 0: y = 0
        if y > height: y = height
        self.y = y

    def moveHorizontal(self, offset):
        y = self.y
        width = self.buffer[y].length()
        x = self.x + offset
        if x < 0: x = 0
        if x > width: x = width
        self.x = x

    def trackHorizontalInsert(self, x, length):
        if x <= self.x: self.x += length

    def trackHorizontalDelete(self, x, length):
        if x < self.x:
            self.x -= length
            if self.x < x: self.x = x

    def trackVerticalInsert(self, y, length):
        if y <= self.y: self.y += length

    def trackVerticalDelete(self, y, length):
        if y < self.y:
            self.y -= length
            if self.y < y: self.y = y


