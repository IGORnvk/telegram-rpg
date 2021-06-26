from fighter import Fighter
from move import UseActiveSkill
from player import Player
from skill import ActiveSkillEffectType


def check_skill_type(skill):
    if skill.effect.type == ActiveSkillEffectType.damage.value:
        return "Урон: {}".format(skill.effect.value)
    if skill.effect.type == ActiveSkillEffectType.heal.value:
        return "Восстанавливает: {}".format(skill.effect.value)
    if skill.effect.type == ActiveSkillEffectType.debuff_defense.value:
        return "Повреждение защиты: {}".format(skill.effect.value)


def print_player_info(player: Player):
    print("Игрок {}:\n\tУровень: {}\n\tЗдоровье: {}\n\tМана: {}".format(player.username,
                                                                        player.level, player.cur_health,
                                                                        player.cur_mana))
    skills = player.active_skills
    print("Активные скиллы:")
    for i, skill in enumerate(skills):
        print("\tНомер: {}\n\t\tНазвание: {}\n\t\tРанг: {}\n\t\tОписание: {}\n\t\t{}".format(i, skill.name, skill.rang,
                                                                                             skill.description,
                                                                                             check_skill_type(skill)))
    skills = player.passive_skills
    print("Пассивные скиллы:")
    for i, skill in enumerate(skills):
        print("\tНомер: {}\n\t\tНазвание: {}\n\t\tРанг: {}\n\t\tОписание: {}\n\t\t{}".format(i, skill.name, skill.rang,
                                                                                             skill.description,
                                                                                             check_skill_type(skill)))

    # print(player.username, player.level, player.cur_health, player.cur_mana, player.equipment, player.active_skills,
    #      player.passive_skills)


class ConsoleGame:
    def __init__(self, player1: Player, player2: Player) -> None:
        self.player1 = player1
        self.player2 = player2
        self.fighter = Fighter(player1, player2)

    def run(self):
        game_over = False
        while not game_over:
            to_move = self.fighter.get_attacker()
            defender = self.fighter.get_defender()
            print_player_info(to_move)
            print_player_info(defender)
            number = int(input())
            print("Выбранный скил: {}".format(to_move.active_skills[number].name))
            is_finished, damage = self.fighter.step(UseActiveSkill(to_move.active_skills[number]))
            print("Нанесенный урон: {}".format(damage))
