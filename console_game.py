from fighter import Fighter
from move import UseActiveSkill
from player import Player


def print_player_info(player: Player):
    print(player.username, player.level, player.cur_health, player.cur_mana, player.equipment, player.active_skills,
          player.passive_skills)


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
            skills = to_move.active_skills
            print_player_info(to_move)
            for skill in skills:
                print(to_move.active_skills, to_move.passive_skills)
            number = int(input())
            self.fighter.step(UseActiveSkill(to_move.active_skills[number]))
            print(to_move.cur_health, to_move.cur_mana, defender.cur_health, defender.cur_mana)
