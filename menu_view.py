import arcade
import arcade.gui

import game_constants as gc

import username_selection_view


class StartButton(arcade.gui.UIFlatButton):
    def __init__(self, window, text, width):
        super().__init__(text=text, width=width)
        self.window = window

    def on_click(self, event: arcade.gui.UIOnClickEvent):
        self.window.show_view(username_selection_view.UsernameSelectionView())


class QuitButton(arcade.gui.UIFlatButton):
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        arcade.exit()


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.v_box = arcade.gui.UIBoxLayout()

        start_button = StartButton(window=self.window, text="Start Game", width=200)
        self.v_box.add(start_button.with_space_around(bottom=20))

        settings_button = arcade.gui.UIFlatButton(text="Settings", width=200)
        self.v_box.add(settings_button.with_space_around(bottom=20))

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
        arcade.draw_text(gc.SCREEN_TITLE, gc.SCREEN_WIDTH / 2, gc.SCREEN_HEIGHT / 3 * 2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        self.manager.draw()
