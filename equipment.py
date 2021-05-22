class Equipment:
    def __init__(self, weapon=None, headgear=None, cuirasses=None, boots=None, gauntlets=None, shield=None,
                 jewelry=None):
        self.weapon = weapon
        self.headgear = headgear
        self.cuirasses = cuirasses
        self.boots = boots
        self.gauntlets = gauntlets
        self.shield = shield
        self.jewelry = jewelry

    def get_total_power(self):
        power = self.weapon.power
        for i in self.jewelry:
            if i.effect_type == 'power':
                power += i.value
        return power

    def get_total_defense(self):
        defense = self.headgear.defense + self.cuirasses.defense + self.boots.defense + self.gauntlets.defense + self.\
            shield.defense
        for i in self.jewelry:
            if i.effect_type == 'defense':
                defense += i.value
        return defense
