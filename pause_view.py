import arcade
import arcade.gui

import game_constants as gc

import game_view


class ResumeButton(arcade.gui.UIFlatButton):
    def __init__(self, current_game_view, window, text, width):
        super().__init__(text=text, width=width)
        self.window = window
        self.current_game_view = current_game_view

    def on_click(self, event: arcade.gui.UIOnClickEvent):
        self.window.show_view(self.current_game_view)


class RestartButton(arcade.gui.UIFlatButton):
    def __init__(self, window, text, width):
        super().__init__(text=text, width=width)
        self.window = window

    def on_click(self, event: arcade.gui.UIOnClickEvent):
        self.window.show_view(game_view.GameView())


class QuitButton(arcade.gui.UIFlatButton):
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        arcade.exit()


class PauseView(arcade.View):
    def __init__(self, current_game_view):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.v_box = arcade.gui.UIBoxLayout()
        self.current_game_view = current_game_view

        resume_button = ResumeButton(current_game_view=self.current_game_view, window=self.window,
                                     text="Resume Game", width=200)
        self.v_box.add(resume_button.with_space_around(bottom=20))

        restart_button = RestartButton(window=self.window, text="Restart", width=200)
        self.v_box.add(restart_button.with_space_around(bottom=20))

        quit_button = QuitButton(text="Quit", width=200)
        self.v_box.add(quit_button)

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                align_y=-96,
                child=self.v_box)
        )

    def on_show_view(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        self.window.clear()
        arcade.draw_text("Game is Paused", gc.SCREEN_WIDTH / 2, gc.SCREEN_HEIGHT / 3 * 2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        self.manager.draw()

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.current_game_view)
