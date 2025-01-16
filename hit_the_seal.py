
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder

class MainScreen(Screen):
    pass

class GameScreen(Screen):
    pass

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

if __name__ == '__main__':
    HitTheSealApp().run()
