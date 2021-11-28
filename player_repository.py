import psycopg2
from psycopg2 import sql

from equipment import Equipment
from inventory import Inventory
from item import Armor, ArmorType, Potion, PotionEffect, PotionEffectType
from player import Player
from skill import ActiveSkill, ActiveSkillEffect, ActiveSkillEffectType, PassiveSkill, PassiveSkillEffect, \
    PassiveSkillEffectType


class PlayerRepository:
    @staticmethod
    def get_player(telegram_id):
        conn = None
        try:
            conn = psycopg2.connect(
                host="localhost",
                database="roleplay",
                user="postgres",
                password="0989117777")
            cur = conn.cursor()
            sql = 'SELECT * from player WHERE telegram_id = %s'
            cur.execute(sql, (telegram_id, ))
            record = cur.fetchone()
            player = Player(
                id=record[1],
                level='46',
                username=record[2],
                max_health=record[3],
                cur_health=record[3],
                power=record[5],
                defense=record[6],
                mana=record[4],
                cur_mana=record[4],
                intelligence=record[7],
                active_skills=PlayerRepository.get_active_skills(record[0]),
                passive_skills=PlayerRepository.get_passive_skills(record[0]),
                equipment=[],
                inventory=[],
                potions=[]
            )
            cur.close()
            return player
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                print('Database connection closed.')

    @staticmethod
    def get_active_skills(player_id):
        conn = None
        try:
            conn = psycopg2.connect(
                host="localhost",
                database="roleplay",
                user="postgres",
                password="0989117777")
            cur = conn.cursor()
            print('PostgreSQL database version:')
            sql = 'SELECT * from active_skill JOIN player_has_active_skill ' \
                  'ON active_skill.id = player_has_active_skill.active_skill_id ' \
                  'WHERE player_id = %s'
            cur.execute(sql, (player_id,))
            records = cur.fetchall()
            active_skills = []
            for record in records:
                active_skill = ActiveSkill(
                    name=record[1],
                    rang=record[2],
                    description=record[3],
                    mana_usage=record[4],
                    effect=record[5]
                )
                active_skills.append(active_skill)
            cur.close()
            return active_skills
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
            print('Database connection closed.')

    @staticmethod
    def get_passive_skills(player_id):
        conn = None
        try:
            conn = psycopg2.connect(
                host="localhost",
                database="roleplay",
                user="postgres",
                password="0989117777")
            cur = conn.cursor()
            print('PostgreSQL database version:')
            sql = 'SELECT passive_skill.id, passive_skill.name, passive_skill.description, passive_skill_effect.meaning,' \
                  ' passive_skill.value from passive_skill ' \
                  'JOIN player_has_passive_skill ON passive_skill.id = player_has_passive_skill.passive_skill_id ' \
                  'JOIN passive_skill_effect ON passive_skill_effect.id = passive_skill.passive_skill_effect_id ' \
                  'WHERE player_id = %s'
            cur.execute(sql, (player_id,))
            records = cur.fetchall()
            passive_skills = []
            for record in records:
                passive_skill = PassiveSkill.passive_skill_from_db(
                    name=record[1],
                    rang=record[2],
                    description=record[3],
                    effect_name=record[4],
                    effect_value=record[5]
                )
                passive_skills.append(passive_skill)
            cur.close()
            return passive_skills
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
            print('Database connection closed.')


if __name__ == '__main__':
    player = PlayerRepository.get_player('720419160')
    print(player.passive_skills)
