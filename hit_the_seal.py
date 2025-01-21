from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout


class MainScreen(Screen):
    pass


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.time_left = 30  
        self.timer_label = Label(
            text = f"Time Left: {self.time_left} s",
            font_size = 24,
            size_hint = (1, 0.2),
            color = (255, 228, 196, 1) ,
            pos_hint = {"center_x": 0.5, "center_y": 0.8},)
        layout = FloatLayout()
        layout.add_widget(self.timer_label)
        self.add_widget(layout)

    def on_enter(self):
        self.time_left = 30  #reset
        self.event = Clock.schedule_interval(self.update_timer, 1)  #update every 1 sec

    def on_leave(self):
        Clock.unschedule(self.event)

    def update_timer(self, dt):
        self.time_left -= 1
        self.timer_label.text = f"Time Left: {self.time_left} s"
        if self.time_left <= 0:
            Clock.unschedule(self.event)  #stop
            self.manager.current = 'end'  #go to EndScreen


class EndScreen(Screen):
    pass


class HitTheSealApp(App):
    def build(self):
        Builder.load_file('hit_the_seal.kv')
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(GameScreen(name='game'))
        sm.add_widget(EndScreen(name='end'))
        return sm
    def play_again(self):
        #add delay 0.5 sec before change screeen
        Clock.schedule_once(self.switch_to_game, 0.5)

    def switch_to_game(self, dt):
        self.root.current = 'game'

    def exit_game(self):
        #add delay 0.5 sec before close this program
        Clock.schedule_once(self.stop_app, 0.5)

    def stop_app(self, dt):
        self.stop()

if __name__ == '__main__':
    HitTheSealApp().run()