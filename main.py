import logging

from random import randint

from kivy.app import App
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivy.vector import Vector

from res.widgets.PyongBall import PyongBall
from res.widgets.PyongPaddle import PyongPaddle


class PyongGame(Widget):
    log = logging.getLogger('Game Log')
    game_paused = False
    win_score = 10

    winner_label = ObjectProperty(None)

    pyong_ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    def game_over(self):
        if self.player1.score >= self.win_score:
            self.winner_label.text = '{}\nWINS!!!'.format(self.player1.name)
            self.game_paused = True
            return True
        elif self.player2.score >= self.win_score:
            self.winner_label.text = '{}\nWINS!!!'.format(self.player2.name)
            self.game_paused = True
            return True
        return False

    def serve_ball(self, switch=True):
        angle = randint(-60, 60)
        if switch:
            angle += 180
        self.pyong_ball.center = self.center
        self.pyong_ball.velocity = Vector(4, 0).rotate(angle)

    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y

    def game_loop(self, elapsed_time):
        self.pyong_ball.move(elapsed_time)

        self.player1.bounce_ball(self.pyong_ball)
        self.player2.bounce_ball(self.pyong_ball)

        # bounce off top and bottom
        if (self.pyong_ball.y < 0) or (self.pyong_ball.top > self.height):
            self.pyong_ball.velocity_y *= -1

        # bounce off left and right
        if self.pyong_ball.center_x < 0:
            self.player2.score += 1
            self.serve_ball(False)
        if self.pyong_ball.center_x > self.width:
            self.player1.score += 1
            self.serve_ball()

    def update(self, dt):
        if not self.game_paused and not self.game_over():
            self.game_loop(dt)


class PyongApp(App):
    def build(self):
        pyong_game = PyongGame()
        pyong_game.serve_ball()
        Clock.schedule_interval(pyong_game.update, 1.0 / 60.0)
        return pyong_game


if __name__ == '__main__':
    PyongApp().run()
