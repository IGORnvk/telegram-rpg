class Player:
    def __init__(self, level, username, max_health, cur_health, power, defense, mana, intelligence, active_skills, passive_skills):
        self.level = level
        self.username = username
        self.max_health = max_health
        self.cur_health = cur_health
        self.power = power
        self.defense = defense
        self.intelligence = intelligence
        self.active_skills = active_skills
        self.passive_skills = passive_skills
        self.mana = mana

    def power_calculator(self):
        all_power = self.power
        for i in self.passive_skills:
            if i.effect.effect_type == 'power':
                all_power += i.effect.value
        return all_power

    def defense_calculator(self):
        all_defense = self.defense
        for i in self.passive_skills:
            if i.effect.effect_type == 'defense':
                all_defense += i.effect.value
        return all_defense
