from item import *
from skill import PassiveSkillEffectType


class Player:
    def __init__(self, level, username, max_health, cur_health, power, defense, mana, cur_mana, intelligence, active_skills,
                 passive_skills, equipment, inventory, potions):
        self.level = level
        self.username = username
        self.max_health = max_health
        self.cur_health = cur_health
        self.power = power
        self.defense = defense
        self.mana = mana
        self.cur_mana = cur_mana
        self.intelligence = intelligence
        self.active_skills = active_skills
        self.passive_skills = passive_skills
        self.equipment = equipment
        self.inventory = inventory
        self.potions = potions

    def power_calculator(self):
        all_power = self.power
        for i in self.passive_skills:
            if i.effect.type == PassiveSkillEffectType.increase_power.value:
                all_power += i.effect.value
        for i in self.potions:
            if i.effect.effect_type == PotionEffectType.power.value:
                all_power += i.effect.value
        return all_power + self.equipment.get_total_power()

    def defense_calculator(self):
        all_defense = self.defense
        for i in self.passive_skills:
            if i.effect.type == PassiveSkillEffectType.increase_defense.value:
                all_defense += i.effect.value
        for i in self.potions:
            if i.effect.effect_type == PotionEffectType.defense.value:
                all_defense += i.effect.value
        return all_defense + self.equipment.get_total_defense()
