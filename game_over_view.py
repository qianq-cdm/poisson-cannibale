import arcade
import arcade.gui

import game_constants as gc

import game_view


class RestartButton(arcade.gui.UIFlatButton):
    def __init__(self, window, text, width):
        super().__init__(text=text, width=width)
        self.window = window

    def on_click(self, event: arcade.gui.UIOnClickEvent):
        self.window.show_view(game_view.GameView())


class QuitButton(arcade.gui.UIFlatButton):
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        arcade.exit()


class GameOverView(arcade.View):
    def __init__(self, did_win: bool, time_taken: str, score: int):
        super().__init__()
        self.game_view = game_view
        self.did_win = did_win
        self.time_taken = time_taken
        self.score = score

        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.v_box = arcade.gui.UIBoxLayout()

        replay_button = RestartButton(window=self.window, text="Replay", width=200)
        self.v_box.add(replay_button.with_space_around(bottom=20))

        quit_button = QuitButton(text="Quit", width=200)
        self.v_box.add(quit_button)

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                align_y=-128,
                child=self.v_box)
        )

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLUE_YONDER)

    def on_draw(self):
        self.window.clear()
        self.manager.draw()
        arcade.draw_text("GAME OVER", gc.SCREEN_WIDTH / 2, gc.SCREEN_HEIGHT / 2 + 50,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        if self.did_win:
            arcade.draw_text("You won the game!",
                             gc.SCREEN_WIDTH / 2,
                             gc.SCREEN_HEIGHT / 2,
                             arcade.color.BLACK,
                             font_size=20,
                             anchor_x="center",
                             width=gc.SCREEN_WIDTH,
                             align="center")
        else:
            arcade.draw_text("You lost all of your lives!",
                             gc.SCREEN_WIDTH / 2,
                             gc.SCREEN_HEIGHT / 2,
                             arcade.color.BLACK,
                             font_size=20,
                             anchor_x="center",
                             width=gc.SCREEN_WIDTH,
                             align="center")

        arcade.draw_text(f"Time taken: {self.time_taken} | Score: {self.score}",
                         gc.SCREEN_WIDTH / 2,
                         512,
                         arcade.color.BLACK,
                         font_size=15,
                         anchor_x="center")
