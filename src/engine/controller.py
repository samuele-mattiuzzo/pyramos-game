# -*- coding: utf-8 -*-


class ControllerMixin:

    def __init__(self):
        self.on_init()

    def on_init(self):
        pass

    def handle_input(self, ui_screen=None, input=None):
        if input:
            if not ui_screen:
                self._handle_game_input(input)
            else:
                self._handle_ui_input(ui_screen, input)

    def _handle_game_input(self, input):
        raise NotImplementedError()

    def _handle_ui_input(self, ui_screen, input):
        raise NotImplementedError()
