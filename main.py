"""
Simple jeu fait avec arcade.
Le jeu consiste a ce que notre poisson mange des poissons plus petits que lui pour grossir.
L'utilisateur doit aussi éviter les poissons plus gros afin de ne pas perdre de vie.
"""
import random

import arcade

from game_time import GameElapsedTime
from player import Player, Direction
from enemy_fish import EnemyFish
from fish_animation import FishAnimation
import game_constants as gc
from game_state import GameState as gs


class MyGame(arcade.Window):
    """
    La classe principale de l'application

    NOTE: Vous pouvez effacer les méthodes que vous n'avez pas besoin.
    Si vous en avez besoin, remplacer le mot clé "pass" par votre propre code.
    """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.BLUE_YONDER)

        self.back_ground = None

        self.game_state = None

        # Player related attributes.
        self.player = None
        self.player_move_up = False
        self.player_move_down = False
        self.player_move_left = False
        self.player_move_right = False

        self.enemy_list = None

        self.life_one = None
        self.life_two = None
        self.life_three = None

        self.game_camera = None
        self.gui_camera = None

        self.game_timer = GameElapsedTime()
        self.time_since_last_accumulate = 0

        self.colliding_with = None

    def setup(self):
        """
        Configurer les variables de votre jeu ici. Il faut appeler la méthode une nouvelle
        fois si vous recommencer une nouvelle partie.
        """
        self.game_state = gs.GAME_RUNNING

        self.player = Player("assets/2dfish/spritesheets/__cartoon_fish_06_yellow_idle.png")
        self.player.current_animation.center_x = 200
        self.player.current_animation.center_y = 200

        self.back_ground = arcade.Sprite("assets/Background.png")
        self.back_ground.center_x = gc.SCREEN_WIDTH / 2
        self.back_ground.center_y = gc.SCREEN_HEIGHT / 2

        self.enemy_list = arcade.SpriteList()

        self.life_one = FishAnimation("assets/2dfish/spritesheets/__cartoon_fish_06_yellow_idle.png", scale=0.10)
        self.life_one.left = 100
        self.life_one.top = gc.SCREEN_HEIGHT - 10
        self.life_two = FishAnimation("assets/2dfish/spritesheets/__cartoon_fish_06_yellow_idle.png", scale=0.10)
        self.life_two.left = self.life_one.right + 10
        self.life_two.top = gc.SCREEN_HEIGHT - 10
        self.life_three = FishAnimation("assets/2dfish/spritesheets/__cartoon_fish_06_yellow_idle.png", scale=0.10)
        self.life_three.left = self.life_two.right + 10
        self.life_three.top = gc.SCREEN_HEIGHT - 10

        self.game_camera = arcade.Camera(gc.SCREEN_WIDTH, gc.SCREEN_HEIGHT)
        self.gui_camera = arcade.Camera(gc.SCREEN_WIDTH, gc.SCREEN_HEIGHT)

        # Each two seconds, a new enemy fish will spawn.
        arcade.schedule(self.spawn_enemy_fish, 2)

    def spawn_enemy_fish(self, delta_time):
        """
        Callback method to spawn a new fish.
        :param delta_time: The elapsed time.
        :return: None
        """
        if not self.game_state == gs.GAME_RUNNING:
            return
        direction = Direction.LEFT if random.randint(0, 1) == 1 else Direction.RIGHT
        x = -50 if direction == Direction.RIGHT else gc.SCREEN_WIDTH + 50
        y = random.randrange(50, gc.SCREEN_HEIGHT - 150)
        enemy = EnemyFish(direction, (x, y))
        
        self.enemy_list.append(enemy)

    def draw_lives(self):
        if self.player.lives >= 1:
            self.life_one.draw()
        if self.player.lives >= 2:
            self.life_two.draw()
        if self.player.lives == 3:
            self.life_three.draw()

    def on_draw(self):
        """
        C'est la méthode que Arcade invoque à chaque "frame" pour afficher les éléments
        de votre jeu à l'écran.
        """
        arcade.start_render()

        # Game camera rendering
        self.game_camera.use()
        self.back_ground.draw()

        self.player.draw()

        self.enemy_list.draw()

        # Gui camera rendering
        self.gui_camera.use()
        arcade.draw_rectangle_filled(gc.SCREEN_WIDTH // 2, gc.SCREEN_HEIGHT - 25, gc.SCREEN_WIDTH, 50, arcade.color.BLEU_DE_FRANCE)

        arcade.draw_text("Lives :", 5, gc.SCREEN_HEIGHT - 35, arcade.color.WHITE_SMOKE, 20, width=100, align="center")
        self.draw_lives()

        arcade.draw_text(
            f"Time played : {self.game_timer.get_time_string()}",
            gc.SCREEN_WIDTH - 350, 
            gc.SCREEN_HEIGHT - 35, 
            arcade.color.WHITE_SMOKE, 
            20, width=400, align="center")

    def on_update(self, delta_time):
        """
        Toute la logique pour déplacer les objets de votre jeu et de
        simuler sa logique vont ici. Normalement, c'est ici que
        vous allez invoquer la méthode "update()" sur vos listes de sprites.
        Paramètre:
            - delta_time : le nombre de milliseconde depuis le dernier update.
        """
        if self.game_state == gs.GAME_RUNNING:
            # Calculate elapsed time
            self.game_timer.accumulate()

            self.player.update(delta_time)
            self.enemy_list.update()

            self.accumulate_score_by_time(delta_time)
            self.collision_detection()
            self.is_alive()

    def collision_detection(self):
        player_hit_list = arcade.check_for_collision_with_list(self.player.current_animation, self.enemy_list)
        for enemy in player_hit_list:
            player_size = self.player.scale
            enemy_size = enemy.scale
            if enemy_size > player_size:
                if enemy == self.colliding_with:
                    return
                self.colliding_with = enemy
                self.player.lives -= 1
            else:
                self.player.scale += 0.05
                self.player.score += enemy.value
                enemy.remove_from_sprite_lists()

    def accumulate_score_by_time(self, delta_time):
        self.time_since_last_accumulate += delta_time
        if self.time_since_last_accumulate >= gc.TIME_FOR_POINTS:
            self.player.score += gc.POINTS_FOR_TIME
            self.time_since_last_accumulate = 0

    def is_alive(self):
        if self.player.lives == 0:
            self.game_state = gs.GAME_OVER

    def update_player_speed(self):
        """
        Will update player position according to various movement flags.
        :return: None
        """
        self.player.current_animation.change_x = 0
        self.player.current_animation.change_y = 0

        if self.player_move_left and not self.player_move_right:
            self.player.change_direction(Direction.LEFT)
            self.player.current_animation.change_x = -Player.MOVEMENT_SPEED
        elif self.player_move_right and not self.player_move_left:
            self.player.change_direction(Direction.RIGHT)
            self.player.current_animation.change_x = Player.MOVEMENT_SPEED

        if self.player_move_up and not self.player_move_down:
            self.player.current_animation.change_y = Player.MOVEMENT_SPEED
        elif self.player_move_down and not self.player_move_up:
            self.player.current_animation.change_y = -Player.MOVEMENT_SPEED

    def on_key_press(self, key, key_modifiers):
        """
        Cette méthode est invoquée à chaque fois que l'usager tape une touche
        sur le clavier.
        Paramètres:
            - key: la touche enfoncée
            - key_modifiers: est-ce que l'usager appuie sur "shift" ou "ctrl" ?

        Pour connaître la liste des touches possibles:
        https://api.arcade.academy/en/latest/arcade.key.html
        """
        if key == arcade.key.A:
            self.player_move_left = True
            self.update_player_speed()
        elif key == arcade.key.D:
            self.player_move_right = True
            self.update_player_speed()
        elif key == arcade.key.W:
            self.player_move_up = True
            self.update_player_speed()
        elif key == arcade.key.S:
            self.player_move_down = True
            self.update_player_speed()

    def on_key_release(self, key, key_modifiers):
        """
        Méthode invoquée à chaque fois que l'usager enlève son doigt d'une touche.
        Paramètres:
            - key: la touche relâchée
            - key_modifiers: est-ce que l'usager appuie sur "shift" ou "ctrl" ?
        """
        if key == arcade.key.A:
            self.player_move_left = False
            self.update_player_speed()
        elif key == arcade.key.D:
            self.player_move_right = False
            self.update_player_speed()
        elif key == arcade.key.W:
            self.player_move_up = False
            self.update_player_speed()
        elif key == arcade.key.S:
            self.player_move_down = False
            self.update_player_speed()


def main():
    """ Main method """
    game = MyGame(gc.SCREEN_WIDTH, gc.SCREEN_HEIGHT, gc.SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
