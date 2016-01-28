from .AbstractAction import AbstractAction
from .Range import Range, Position
from .Logger import debug


class GotoTop(AbstractAction):
    def act(self, callback = None):
        y = self.command.multiplyAll()
        motion = self.motions.gotoPositionStrict(Position(y,1))
        if callback:
            return callback.call(motion.linewise())
        else:
            self.cursor.move(motion)
            self.finish()
            return "normal", self.actionManager.action("normal", "idle")

