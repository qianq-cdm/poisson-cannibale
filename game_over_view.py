import arcade
import game_constants as gc

class GameOverView(arcade.View):
    def __init__(self, game_view, did_win: bool, time_taken: str, score: int):
        super().__init__()
        self.game_view = game_view
        self.did_win = did_win
        self.time_taken = time_taken
        self.score = score

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLUE_YONDER)

    def on_draw(self):
        self.window.clear()
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
