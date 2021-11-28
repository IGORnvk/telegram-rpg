import enum


class Skill:
    def __init__(self, name, rang, description):
        self.name = name
        self.rang = rang
        self.description = description


class PassiveSkillEffectType(enum.Enum):
    increase_power = 0
    increase_defense = 1
    increase_mana = 2


class PassiveSkillEffect:
    def __init__(self, value, type: PassiveSkillEffectType):
        self.value = value
        self.type = type

    @staticmethod
    def passive_skill_effect_from_db(effect_name, value):
        effect_type = -1

        if effect_name == "increase_power":
            effect_type = PassiveSkillEffectType.increase_power.value
        elif effect_name == "increase_defense":
            effect_type = PassiveSkillEffectType.increase_defense.value
        elif effect_name == "increase_mana":
            effect_type = PassiveSkillEffectType.increase_mana.value

        assert effect_type != -1, \
            "effect_name should have an appropriate value!"

        return PassiveSkillEffect(value, effect_type)
        

class PassiveSkill(Skill):
    def __init__(self, name, rang, description, effect: PassiveSkillEffect):
        Skill.__init__(self, name, rang, description)
        self.effect = effect

    def __repr__(self):
        return f"{self.name}, {self.rang}, {self.description}, {self.effect}"

    @staticmethod
    def passive_skill_from_db(name, rang, description, effect_name, effect_value):
        return PassiveSkill(
            name=name,
            rang=rang,
            description=description,
            effect=PassiveSkillEffect.passive_skill_effect_from_db(effect_name, effect_value)
        )


class ActiveSkillEffectType(enum.Enum):
    damage = 0
    heal = 1
    debuff_defense = 2


class ActiveSkillEffect:
    def __init__(self, value, type: ActiveSkillEffectType):
        self.value = value
        self.type = type
        

class ActiveSkill(Skill):
    def __init__(self, name, rang, description, mana_usage, effect: ActiveSkillEffect):
        Skill.__init__(self, name, rang, description)
        self.mana_usage = mana_usage
        self.effect = effect

    def __repr__(self):
        return f'{self.name}, {self.rang}, {self.description}, {self.mana_usage}, {self.effect}'
