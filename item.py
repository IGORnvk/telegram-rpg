import enum


class Item:
    def __init__(self, name):
        self.name = name


class Weapon(Item):
    def __init__(self, name, rang, power):
        Item.__init__(self, name)
        self.rang = rang
        self.power = power


class ArmorType(enum.Enum):
    headgear = 0
    cuirasses = 1
    boots = 2
    gauntlets = 3
    shield = 4


class Armor(Item):
    def __init__(self, name, rang, defense, armor_type: ArmorType):
        Item.__init__(self, name)
        self.rang = rang
        self.defense = defense
        self.armor_type = armor_type


class PotionEffectType(enum.Enum):
    power = 0
    defense = 1
    health = 2
    mana = 3


class PotionEffect:
    def __init__(self, value, effect_type: PotionEffectType):
        self.value = value
        self.effect_type = effect_type


class Potion(Item):
    def __init__(self, name, rang, effect: PotionEffect):
        Item.__init__(self, name)
        self.rang = rang
        self.effect = effect


class AccessoriesEffectType(enum.Enum):
    power = 0
    defense = 1


class AccessoriesEffect:
    def __init__(self, value, effect_type: AccessoriesEffectType):
        self.value = value
        self.effect_type = effect_type


class Accessories(Item):
    def __init__(self, name, rang, effect: AccessoriesEffect):
        Item.__init__(self, name)
        self.rang = rang
        self.effect = effect


