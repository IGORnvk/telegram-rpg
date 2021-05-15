class Skill:
    def __init__(self, skill_type, name, rang, description, mana_usage, effect):
        self.name = name
        self.rang = rang
        self.description = description
        self.mana_usage = mana_usage
        self.effect = effect
        self.skill_type = skill_type


# types of active skills:
#                        damage
#                        heal
#                        debuff defense
# types of passive skills:
#                        characteristic increase
class Effect:
    def __init__(self, effect_type, value):
        self.effect_type = effect_type
        self.value = value
