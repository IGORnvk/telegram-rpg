from item import Potion
from skill import *

class Move:
    def __init__(self):
        pass


class UseActiveSkill(Move):
    def __init__(self, active_skill: ActiveSkill):
        super().__init__()
        self.active_skill = active_skill

class UsePotion(Move):
    def __init__(self, potion: Potion):
        super().__init__()
        self.potion = potion