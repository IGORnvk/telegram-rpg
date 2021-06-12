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
        

class PassiveSkill(Skill):
    def __init__(self, name, rang, description, effect: PassiveSkillEffect):
        Skill.__init__(self, name, rang, description)
        self.effect = effect


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



# types of active skills:
#                        damage
#                        heal //TODO
#                        debuff defense //TODO
# types of passive skills:
#                        characteristic increase