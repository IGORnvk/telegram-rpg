import enum


class Item:
    def __init__(self, name, item_id):
        self.name = name
        self.item_id = item_id


class Weapon(Item):
    def __init__(self, name, rang, power, item_id):
        Item.__init__(self, name, item_id)
        self.rang = rang
        self.power = power


class ArmorType(enum.Enum):
    headgear = 0
    cuirasses = 1
    boots = 2
    gauntlets = 3
    shield = 4

    @staticmethod
    def armor_type_from_name(armor_type_name):
        armor_type = -1

        if armor_type_name == 'headgear':
            armor_type = ArmorType.headgear.value
        if armor_type_name == 'cuirasses':
            armor_type = ArmorType.cuirasses.value
        if armor_type_name == 'boots':
            armor_type = ArmorType.boots.value
        if armor_type_name == 'gauntlets':
            armor_type = ArmorType.gauntlets.value
        if armor_type_name == 'shield':
            armor_type = ArmorType.shield.value

        assert armor_type != -1, \
            "armor_type_name should have an appropriate value!"

        return armor_type


class Armor(Item):
    def __init__(self, name, rang, defense, armor_type: ArmorType, item_id):
        Item.__init__(self, name, item_id)
        self.rang = rang
        self.defense = defense
        self.armor_type = armor_type

    @staticmethod
    def armor_from_db(name, rang, defense, armor_type_name, item_id):
        return Armor(
            name=name,
            rang=rang,
            defense=defense,
            armor_type=ArmorType.armor_type_from_name(armor_type_name),
            item_id=item_id
        )


class PotionEffectType(enum.Enum):
    power = 0
    defense = 1
    health = 2
    mana = 3


class PotionEffect:
    def __init__(self, value, effect_type: PotionEffectType):
        self.value = value
        self.effect_type = effect_type

    @staticmethod
    def potion_effect_type(effect_name, value):
        effect_type = -1

        if effect_name == 'power':
            effect_type = PotionEffectType.power.value
        if effect_name == 'defense':
            effect_type = PotionEffectType.defense.value
        if effect_name == 'health':
            effect_type = PotionEffectType.health.value
        if effect_name == 'mana':
            effect_type = PotionEffectType.mana.value

        assert effect_type != -1, \
            "armor_type_name should have an appropriate value!"

        return PotionEffect(value, PotionEffectType(effect_type))

    def __repr__(self):
        return f'{self.value},  {self.effect_type.name}'


class Potion(Item):
    def __init__(self, name, rang, effect: PotionEffect, item_id=-1):
        Item.__init__(self, name, item_id)
        self.rang = rang
        self.effect = effect

    @staticmethod
    def potion_from_db(name, rang, effect_name, effect_value):
        return Potion(
            name=name,
            rang=rang,
            effect=PotionEffect.potion_effect_type(effect_name, effect_value)
        )

    def __repr__(self):
        return f'{self.name}, {self.rang}, {self.effect}'


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
