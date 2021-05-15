from player import *
from skill import *
from fighter import *

player1 = Player(10, 'Ivan', 63, 63, 20, 15, 14, 10, [Skill('active', 'knife', 'F', 'first skill', 5, Effect('damage', 15))],
                 [Skill('passive', 'power increase', 'F', 'first passive skill', 2, Effect('power', 5))])
player2 = Player(12,'Igor', 60, 60, 21, 16, 19, 11, [Skill('active', 'knife', 'F', 'first skill', 5, Effect('damage', 15))],
                 [Skill('passive', 'defense increase', 'F', 'increases your defense', 3, Effect('defense', 6))])
fighter = Fighter(player1, player2)
while True:
    is_finished, damage = fighter.step(player1.active_skills[0])
    print(damage, player1.mana, player2.mana, player1.cur_health, player2.cur_health)
    if is_finished:
        break
