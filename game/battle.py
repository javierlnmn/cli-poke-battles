import random
import time

import clear_screen
import questionary

from config.config import (
    ATTACK_TYPE_KEYWORD_DAMAGE,
    ATTACK_TYPE_KEYWORD_EFFECT,
    ATTACK_TYPE_KEYWORD_STATUS,
    DEFAULT_HEALTH_BAR_LENGTH,
    DEFAULT_SPACE_BETWEEN_SPRITES,
    POKEMON_AFFECTED_KEYWORD_ENEMY,
    POKEMON_AFFECTED_KEYWORD_SELF,
    POKEMON_STAT_KEYWORD_ATTACK_PHYSICAL,
    POKEMON_STAT_KEYWORD_ATTACK_SPECIAL,
    POKEMON_STAT_KEYWORD_DEFENSE_PHYSICAL,
    POKEMON_STAT_KEYWORD_DEFENSE_SPECIAL,
)
from game.pokemon import Pokemon
from utils.ascii_art import (
    print_full_screen_title_animation,
    reset_console_color,
    set_console_color,
)


class Battle:
    def __init__(self, pokemon_1: Pokemon, pokemon_2: Pokemon):
        self.pokemon_1 = pokemon_1
        self.pokemon_2 = pokemon_2
        self.winner = None
        self.starting_pokemon = (
            pokemon_1
            if pokemon_1.stats["speed"] >= pokemon_2.stats["speed"]
            else pokemon_2
        )
        self.turn = 1 if self.starting_pokemon is pokemon_1 else 2

    def get_battle_state(self):

        battle_state = "\n".join(
            [
                row[0] + (" ") * DEFAULT_SPACE_BETWEEN_SPRITES + row[1]
                for row in zip(
                    self.pokemon_1.get_visual_stats_sprite().split("\n"),
                    self.pokemon_2.get_visual_stats_sprite().split("\n"),
                )
            ]
        )

        return battle_state

    def switch_turn(self):
        self.turn = 3 - self.turn

    def play_battle(self):

        while not self.winner:
            clear_screen.clear()
            time.sleep(0.5)

            if self.turn == 1:
                print(self.get_battle_state() + ("\n") * 2)
                print("What should " + str(self.pokemon_1) + " do?")

                pokemon_1_attack_visible_names_list = (
                    self.pokemon_1.get_moves_visible_name_list()
                )

                selected_move_visible_name = questionary.select(
                    "", choices=pokemon_1_attack_visible_names_list
                ).ask()

                selected_attack = self.pokemon_1.get_move_by_visible_name(
                    selected_move_visible_name
                )
                clear_screen.clear()
                time.sleep(0.8)

                print(
                    str(self.pokemon_1) + " used " + selected_attack.visible_name + "!"
                )
                time.sleep(1.2)

                move_hit = self.check_move_hit(selected_attack.accuracy)

                if move_hit:
                    clear_screen.clear()
                    self.use_move(self.pokemon_1, selected_attack, self.pokemon_2)
                else:
                    print(
                        f"But it {set_console_color('red')}failed{reset_console_color()}!"
                    )
                    time.sleep(1.2)
                    clear_screen.clear()

            elif self.turn == 2:
                print(self.get_battle_state() + ("\n"))

                selected_attack = self.pokemon_2.pick_random_move()

                time.sleep(0.8)

                print(
                    (" " * (DEFAULT_HEALTH_BAR_LENGTH + DEFAULT_SPACE_BETWEEN_SPRITES))
                    + str(self.pokemon_2)
                    + " used "
                    + selected_attack.visible_name
                    + "!"
                )
                time.sleep(1.2)

                move_hit = self.check_move_hit(selected_attack.accuracy)

                if move_hit:
                    clear_screen.clear()
                    self.use_move(self.pokemon_2, selected_attack, self.pokemon_1)
                else:
                    print(
                        f"But it {set_console_color('red')}failed{reset_console_color()}!"
                    )
                    time.sleep(1.2)
                    clear_screen.clear()

            if self.pokemon_1.current_hp <= 0:
                self.winner = self.pokemon_2
                break

            if self.pokemon_2.current_hp <= 0:
                self.winner = self.pokemon_1
                break

            self.switch_turn()

        time.sleep(1.2)
        print(self.get_battle_state() + ("\n") * 2)
        print(str(self.winner) + " won the battle!")
        time.sleep(2)
        clear_screen.clear()

        print_full_screen_title_animation("End")
        clear_screen.clear()

    def check_move_hit(self, accuracy):

        hitting_factor = random.randint(1, 100)

        if accuracy < hitting_factor:
            return False

        return True

    def use_move(self, attacker, move, reciever):

        if POKEMON_AFFECTED_KEYWORD_ENEMY in move.pokemon_affected:
            for attack_type in move.pokemon_affected[POKEMON_AFFECTED_KEYWORD_ENEMY]:
                if attack_type == ATTACK_TYPE_KEYWORD_DAMAGE:
                    if (
                        POKEMON_STAT_KEYWORD_ATTACK_SPECIAL
                        in move.pokemon_affected[POKEMON_AFFECTED_KEYWORD_ENEMY][
                            ATTACK_TYPE_KEYWORD_DAMAGE
                        ]
                    ):
                        absolute_damage_dealt = self.calculate_attack_damage(
                            attacker.stats[POKEMON_STAT_KEYWORD_ATTACK_SPECIAL],
                            move.pokemon_affected[POKEMON_AFFECTED_KEYWORD_ENEMY][
                                ATTACK_TYPE_KEYWORD_DAMAGE
                            ][POKEMON_STAT_KEYWORD_ATTACK_SPECIAL],
                            reciever.stats[POKEMON_STAT_KEYWORD_DEFENSE_SPECIAL],
                        )

                        reciever.current_hp = (
                            (reciever.current_hp - absolute_damage_dealt)
                            if absolute_damage_dealt <= reciever.current_hp
                            else 0
                        )

                    elif (
                        POKEMON_STAT_KEYWORD_ATTACK_PHYSICAL
                        in move.pokemon_affected[POKEMON_AFFECTED_KEYWORD_ENEMY][
                            ATTACK_TYPE_KEYWORD_DAMAGE
                        ]
                    ):
                        absolute_damage_dealt = self.calculate_attack_damage(
                            attacker.stats[POKEMON_STAT_KEYWORD_ATTACK_PHYSICAL],
                            move.pokemon_affected[POKEMON_AFFECTED_KEYWORD_ENEMY][
                                ATTACK_TYPE_KEYWORD_DAMAGE
                            ][POKEMON_STAT_KEYWORD_ATTACK_PHYSICAL],
                            reciever.stats[POKEMON_STAT_KEYWORD_DEFENSE_PHYSICAL],
                        )

                        reciever.current_hp = (
                            (reciever.current_hp - absolute_damage_dealt)
                            if absolute_damage_dealt <= reciever.current_hp
                            else 0
                        )

                elif attack_type == ATTACK_TYPE_KEYWORD_EFFECT:
                    time.sleep(1.2)

                    for stat in move.pokemon_affected[POKEMON_AFFECTED_KEYWORD_ENEMY][
                        ATTACK_TYPE_KEYWORD_EFFECT
                    ]:
                        multiplier = move.pokemon_affected[
                            POKEMON_AFFECTED_KEYWORD_ENEMY
                        ][ATTACK_TYPE_KEYWORD_EFFECT][stat]
                        reciever.stats[stat] *= multiplier
                        verb = (
                            (
                                set_console_color("green")
                                + "increased"
                                + reset_console_color()
                            )
                            if multiplier > 1
                            else (
                                set_console_color("red")
                                + "decreased"
                                + reset_console_color()
                            )
                        )
                        percentage = (
                            round((multiplier - 1) * 100)
                            if multiplier > 1
                            else round((1 - multiplier) * 100)
                        )
                        print(
                            f"{reciever.visible_name}'s {stat} {verb} by {percentage}%"
                        )

                    time.sleep(2)

                elif attack_type == ATTACK_TYPE_KEYWORD_STATUS:
                    time.sleep(1.2)

                    for status in move.pokemon_affected[POKEMON_AFFECTED_KEYWORD_ENEMY][
                        ATTACK_TYPE_KEYWORD_STATUS
                    ]:
                        status_data = move.pokemon_affected[
                            POKEMON_AFFECTED_KEYWORD_ENEMY
                        ][ATTACK_TYPE_KEYWORD_STATUS][status]

                else:
                    clear_screen.clear()
                    print(
                        "Attack type not defined. Please review the attack data in pokemon_data.json file."
                    )
                    time.sleep(2)

        if POKEMON_AFFECTED_KEYWORD_SELF in move.pokemon_affected:
            print(move.pokemon_affected[POKEMON_AFFECTED_KEYWORD_SELF])

    def calculate_attack_damage(
        self,
        attacker_attack,
        move_attack,
        reciever_defense,
        attacker_modifier=1,
        reciever_modifier=1,
    ):
        total_damage = attacker_attack * (
            (attacker_attack * attacker_modifier / reciever_defense * reciever_modifier)
            * 0.3
        )
        return 1 if total_damage <= 1 else round(total_damage)
