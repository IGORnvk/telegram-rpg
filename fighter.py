from item import PotionEffectType
from move_effect import AttackEffect, IncreaseHealthEffect, IncreaseManaEffect, IncreaseDefenseEffect, \
    IncreasePowerEffect
from skill import *
from move import *


class Fighter:
    def __init__(self, predator, victim):
        self.predator = predator
        self.victim = victim
        self.cur_attacker = 1
        self.is_finished = False

    def get_attacker(self):
        if self.cur_attacker == 0:
            return self.victim
        return self.predator

    def get_defender(self):
        if self.cur_attacker == 0:
            return self.predator
        return self.victim

    def step(self, move: Move):
        attacker = self.predator
        defender = self.victim
        if self.cur_attacker == 0:
            attacker = self.victim
            defender = self.predator
        self.cur_attacker = 1 - self.cur_attacker
        if type(move) is UseActiveSkill:
            active_skill = move.active_skill
            if active_skill.effect.type == ActiveSkillEffectType.damage.value:
                power = attacker.power_calculator()
                defense = defender.defense_calculator()
                assert attacker.cur_mana >= active_skill.mana_usage, 'Маны слишком мало!'
                attacker.cur_mana -= active_skill.mana_usage
                damage_dealt = damage(power, defense, active_skill.effect.value)
                defender.cur_health -= damage_dealt

                if defender.cur_health <= 0:
                    self.is_finished = True
                return AttackEffect(damage_dealt, self.is_finished)

            if active_skill.effect.type == ActiveSkillEffectType.heal.value:
                old_value = attacker.cur_health
                attacker.cur_health += active_skill.effect.value
                if attacker.cur_health >= attacker.max_health:
                    attacker.cur_health = attacker.max_health
                return IncreaseHealthEffect(attacker.cur_health - old_value, False)
        elif type(move) is UsePotion: 
            potion = move.potion
            for i, cur_potion in enumerate(attacker.inventory.items):
                if potion.name == cur_potion.name:
                    del attacker.inventory.items[i]
                    print("Зелье успешно использовано.")
                    break
            if potion.effect.effect_type == PotionEffectType.power.value:
                attacker.potions.append(potion)
                return IncreasePowerEffect(potion.effect.value, False)
            if potion.effect.effect_type == PotionEffectType.defense.value:
                attacker.potions.append(potion)
                return IncreaseDefenseEffect(potion.effect.value, False)
            if potion.effect.effect_type == PotionEffectType.health.value:
                old_value = attacker.cur_health
                attacker.cur_health += potion.effect.value
                if attacker.cur_health >= attacker.max_health:
                    attacker.cur_health = attacker.max_health
                return IncreaseHealthEffect(attacker.cur_health - old_value, False)
            if potion.effect.effect_type == PotionEffectType.mana.value:
                old_value = attacker.cur_mana
                attacker.cur_mana += potion.effect.value
                if attacker.cur_mana >= attacker.mana:
                    attacker.cur_mana = attacker.mana
                return IncreaseManaEffect(attacker.cur_mana - old_value, False)

        return False, 0


def damage(power, defense, skill_damage):
    if power >= defense:
        damage_dealt = skill_damage * (1 + 0.1 * (power - defense))
    else:
        damage_dealt = skill_damage / (1 + 0.1 * (defense - power))
    return damage_dealt
