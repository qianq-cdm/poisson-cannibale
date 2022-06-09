import arcade
import arcade.gui

import game_constants as gc

import game_view


class StartGameButton(arcade.gui.UIFlatButton):
    def __init__(self, window, text, width, username_field):
        super().__init__(text=text, width=width)
        self.window = window
        self.username_field = username_field
        self.username = None

    def process_username(self):
        self.username.split()
        if len(self.username) < 1:
            self.username = "Player"
        elif len(self.username) > 15:
            self.username = self.username[:15]

    def on_click(self, event: arcade.gui.UIOnClickEvent):
        self.username = self.username_field.text
        self.process_username()
        self.window.show_view(game_view.GameView(username=self.username))


class UsernameSelectionView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.v_box = arcade.gui.UIBoxLayout()

        self.username_field = arcade.gui.UIInputText(x=gc.SCREEN_WIDTH / 2 - 75, y=gc.SCREEN_HEIGHT / 2,
                                                     width=250, height=24, text_color=arcade.color.BLACK)

        start_game_button = StartGameButton(window=self.window, text="Start Game", width=200,
                                            username_field=self.username_field)
        self.v_box.add(start_game_button.with_space_around(bottom=20))

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                align_y=-96,
                child=self.v_box)
        )

        self.manager.add(self.username_field)

    def on_show_view(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        self.window.clear()
        arcade.draw_text("Enter your username: ", gc.SCREEN_WIDTH / 12, gc.SCREEN_HEIGHT / 2,
                         arcade.color.BLACK, font_size=24, anchor_x="left")
        arcade.draw_rectangle_outline(self.username_field.center_x, self.username_field.center_y,
                                      width=self.username_field.width + 10, height=self.username_field.height + 10,
                                      color=arcade.color.BLACK)
        self.manager.draw()
