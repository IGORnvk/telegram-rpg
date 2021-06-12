class Equipment:
    def __init__(self, weapon=None, headgear=None, cuirasses=None, boots=None, gauntlets=None, shield=None,
                 jewelry=[]):
        self.weapon = weapon
        self.headgear = headgear
        self.cuirasses = cuirasses
        self.boots = boots
        self.gauntlets = gauntlets
        self.shield = shield
        self.jewelry = jewelry

    def get_total_power(self):
        power = 0 if self.weapon is None else self.weapon.power
        for i in self.jewelry:
            if i.effect_type == 'power':
                power += i.value
        return power

    def get_total_defense(self):
        defense = 0
        if self.headgear is not None:
            defense += self.headgear.defense
        if self.cuirasses is not None:
            defense += self.cuirasses.defense
        if self.boots is not None:
            defense += self.boots.defense
        if self.gauntlets is not None:
            defense += self.gauntlets.defense
        if self.shield is not None:
            defense += self.shield.defense
        for i in self.jewelry:
            if i.effect_type == 'defense':
                defense += i.value
        return defense
