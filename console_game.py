from fighter import Fighter
from player import Player


class ConsoleGame:
    def __init__(self, player1: Player, player2: Player) -> None:
        self.player1 = player1
        self.player2 = player2
        self.fighter = Fighter(player1, player2)
    
    def print_player_info(player):
        pass 


    def run(self):
        game_over = False
        while (not game_over):
            to_move = self.fighter.get_attacker()
            defender = self.fighter.get_defender()
            skills = to_move.active_skills
            # TODO player's info
            for skill in skills:
                pass # TODO print skills list
            number = int(input())
            # TODO choose skill skill[number] 
            # TODO print result of move
