from enum import Enum

from fish_animation import FishAnimation
import game_constants as gc


class Direction(Enum):
    """
    Simple direction enum for left and right.
    """
    LEFT = 0
    RIGHT = 1


class Player:
    """
    Player class for the fish!
    """
    MOVEMENT_SPEED = 5.0
    PLAYER_LIVES = 3
    
    def __init__(self, spritesheet_path):
        self.scale = 0.10
        self.score = 0

        self.left_animation = FishAnimation(spritesheet_path, scale=self.scale)
        self.right_animation = FishAnimation(spritesheet_path, flip=True, scale=self.scale)
        self.current_animation = None

        self.direction = Direction.LEFT
        if self.direction == Direction.LEFT:
            self.current_animation = self.left_animation
        else:
            self.current_animation = self.right_animation

        self.lives = Player.PLAYER_LIVES

    def draw(self):
        self.current_animation.draw()

    def update(self, delta_time):      
        self.current_animation.center_x += self.current_animation.change_x

        if self.current_animation.center_x <= 0:
            self.current_animation.center_x = gc.SCREEN_WIDTH
        elif self.current_animation.center_x >= gc.SCREEN_WIDTH:
            self.current_animation.center_x = 0

        if (not (self.current_animation.bottom <= 0 and self.current_animation.change_y < 0)) and \
                (not (self.current_animation.top >= gc.GUI_HEIGHT and self.current_animation.change_y > 0)):
            self.current_animation.center_y += self.current_animation.change_y

        self.current_animation.scale = self.scale

        self.current_animation.on_update(delta_time)

    def change_direction(self, new_direction):
        """
        Used to update the animation according to the direction.
        :param new_direction: The new direction.
        :return: None
        """
        old_direction = self.direction
        if old_direction == new_direction:
            return
        self.direction = new_direction
        if self.direction == Direction.LEFT:
            self.left_animation.center_x = self.current_animation.center_x
            self.left_animation.center_y = self.current_animation.center_y
            self.current_animation = self.left_animation
        else:
            self.right_animation.center_x = self.current_animation.center_x
            self.right_animation.center_y = self.current_animation.center_y            
            self.current_animation = self.right_animation      
