import time

import clear_screen

from game.battle import Battle
from game.pokemon import random_pokemon, user_choose_pokemon
from utils.ascii_art import print_full_screen_title_animation


class Game:

    @staticmethod
    def play():
        selected_pokemon = user_choose_pokemon()
        clear_screen.clear()
        time.sleep(.8)

        print("You chose " + str(selected_pokemon) + "!")
        print(selected_pokemon.get_ascii_art_color())
        time.sleep(1.5)
        clear_screen.clear()
        time.sleep(0.8)

        enemy_pokemon = random_pokemon()
        print("Oh!")
        time.sleep(1.5)
        clear_screen.clear()
        time.sleep(0.8)

        print("A wild " + str(enemy_pokemon) + " appeared!")
        print(enemy_pokemon.get_ascii_art_color())
        time.sleep(1.5)
        clear_screen.clear()
        time.sleep(0.8)

        print_full_screen_title_animation("Battle!")

        current_battle = Battle(selected_pokemon, enemy_pokemon)

        current_battle.play_battle()

        clear_screen.clear()
        time.sleep(0.8)
