import arcade
import game_constants as gc

class GameOverView(arcade.View):
    def __init__(self, game_view, did_win: bool):
        super().__init__()
        self.game_view = game_view
        self.did_win = did_win

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLUE_YONDER)

    def on_draw(self):
        self.window.clear()
        arcade.draw_text("GAME OVER", gc.SCREEN_WIDTH / 2, gc.SCREEN_HEIGHT / 2 + 50,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
