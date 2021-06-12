from skill import SkillType


class Fighter:
    def __init__(self, predator, victim):
        self.predator = predator
        self.victim = victim
        self.cur_attacker = 1
        self.is_finished = False

    def step(self, active_skill):
        attacker = self.predator
        defender = self.victim
        if self.cur_attacker == 0:
            attacker = self.victim
            defender = self.predator
        if active_skill.effect.skill_type == SkillType.damage.value:
            power = attacker.power_calculator()
            defense = defender.defense_calculator()
            assert attacker.mana >= active_skill.mana_usage, 'Маны слишком мало!'
            attacker.mana -= active_skill.mana_usage
            damage_dealt = damage(power, defense, active_skill.effect.value)
            defender.cur_health -= damage_dealt
            if defender.cur_health <= 0:
                self.is_finished = True
            self.cur_attacker = 1 - self.cur_attacker
            return self.is_finished, damage_dealt
        if active_skill.effect.skill_type == SkillType.heal.value:
            attacker.cur_health += active_skill.effect.value
            if attacker.cur_health >= attacker.max_health:
                attacker.cur_health = attacker.max_health


def damage(power, defense, skill_damage):
    if power >= defense:
        damage_dealt = skill_damage * (1 + 0.1 * (power - defense))
    else:
        damage_dealt = skill_damage / (1 + 0.1 * (defense - power))
    return damage_dealt
