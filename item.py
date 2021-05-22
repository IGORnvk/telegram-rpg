class Item:
    def __init__(self, name):
        self.name = name


class Weapon(Item):
    def __init__(self, name, rang, power):
        Item.__init__(self, name)
        self.rang = rang
        self.power = power


class Armor(Item):
    def __init__(self, name, rang, defense):
        Item.__init__(self, name)
        self.rang = rang
        self.defense = defense


class Potion(Item):
    def __init__(self, name, rang, effect):
        Item.__init__(self, name)
        self.rang = rang
        self.effect = effect


class PotionEffect:
    def __init__(self, value, effect_type):
        self.value = value
        self.effect_type = effect_type


class Accessories(Item):
    def __init__(self, name, rang, effect):
        Item.__init__(self, name)
        self.rang = rang
        self.effect = effect


class AccessoriesEffect:
    def __init__(self, value, effect_type):
        self.value = value
        self.effect_type = effect_type
