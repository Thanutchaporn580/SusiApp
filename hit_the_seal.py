from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.core.audio import SoundLoader
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from random import randint
from functools import partial

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_music = SoundLoader.load('mainbackground_music.mp3')
        if self.background_music:
            self.background_music.loop = False  # Disable looping
            self.background_music.bind(on_stop=self.play_music_again)  # Bind on_stop event

    def on_enter(self):
        if self.background_music and App.get_running_app().sound_enabled:
            self.background_music.play()  

    def on_leave(self):
        if self.background_music:
            self.background_music.stop()

    def play_music_again(self, instance):
        if self.manager.current == 'main' and App.get_running_app().sound_enabled:  # Check if still on the main screen and sound is enabled
            self.background_music.play()

class RulesGameScreen(Screen):
    pass

class LevelScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.level_music = SoundLoader.load('select_level_music.mp3')
        if self.level_music:
            self.level_music.loop = True  # Enable looping

    def on_enter(self):
        if self.level_music and App.get_running_app().sound_enabled:
            self.level_music.play()

    def on_leave(self):
        if self.level_music:
            self.level_music.stop()

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.time_up_sound = SoundLoader.load('breaktime.mp3') 
        self.game_music = SoundLoader.load('retro_game.mp3')
        if self.game_music:
            self.game_music.loop = True  # Enable looping
        self.time_left = 30 
        self.score = 0  
        self.timer_label = Label(
            text = f"Time Left: {self.time_left} s",
            font_size = 24,
            size_hint = (1, 0.3),
            color = (0, 0, 0, 1) ,
            pos_hint = {"center_x": 0.5, "center_y": 0.9},)
        self.score_label = Label(  # Add score label
            text = f"Score: {self.score}",
            font_size = 24,
            size_hint = (1, 0.3),
            color = (1, 0.89, 0.77, 1),
            pos_hint = {"center_x": 0.5, "center_y": 0.8},)
        layout = FloatLayout()
        layout.add_widget(self.timer_label)
        layout.add_widget(self.score_label)  # Add score label to layout
        self.add_widget(layout)
        self.seals = []
        self.level = 1

    def on_enter(self):
        self.time_left = 30  #reset
        self.event = Clock.schedule_interval(self.update_timer, 1)  #update every 1 sec
        self.start_game()
        if self.game_music and App.get_running_app().sound_enabled:
            self.game_music.play() # play sound

    def on_leave(self):
        Clock.unschedule(self.event)
        for seal in self.seals:
            self.remove_widget(seal)
        self.seals.clear()
        if self.game_music:
            self.game_music.stop() # stop music when exit from this screen

    def leave_game(self):
        end_screen = self.manager.get_screen('end')
        end_screen.ids.final_score_label.text = f"Score: {self.score}"
        self.manager.current = 'end'

    def update_timer(self, dt):
        self.time_left -= 1
        self.timer_label.text = f"Time Left: {self.time_left} s"
        if self.time_left <= 0:
            Clock.unschedule(self.event) #stop
            if self.time_up_sound:  # Check if the sound is loaded
                self.time_up_sound.play()  # Play the sound
                # Bind to the `on_stop` event to switch screens when sound finishes
                self.time_up_sound.bind(on_stop=self.switch_to_end_screen)

    def switch_to_end_screen(self, instance):
        end_screen = self.manager.get_screen('end')
        end_screen.ids.final_score_label.text = f"Score: {self.score}"
        self.manager.current = 'end'

    def choose_level(self):
        Clock.schedule_once(self.switch_to_level_select, 0.5)

    def switch_to_level_up(self, dt):
        self.manager.current = 'level_select'

    def start_game(self):
        num_seals = self.level * 1  # Increase number of seals with level
        for _ in range(num_seals):
            self.spawn_seal()

    def spawn_seal(self):
        seal = Image(source='seal.png', size_hint=(0.2, 0.2))
    # Define the safe area for spawning seals
        safe_area_x = (int(self.width * 0.1), int(self.width * 0.9 - seal.width))
        safe_area_y = (int(self.height * 0.3), int(self.height * 0.7 - seal.height))  # Avoid top 30% and bottom 30%
        seal.pos = (randint(*safe_area_x), randint(*safe_area_y))
        seal.bind(on_touch_down=self.hit_seal)  # Bind touch event to hit_seal function
        self.seals.append(seal)
        self.add_widget(seal)
        interval = 7.0 / self.level 
        Clock.schedule_interval(partial(self.move_seal, seal), interval)
    
    def move_seal(self, seal, dt):
        safe_area_x = (int(self.width * 0.1), int(self.width * 0.9 - seal.width))
        safe_area_y = (int(self.height * 0.3), int(self.height * 0.7 - seal.height))  # Avoid top 30% and bottom 30%
        seal.pos = (randint(*safe_area_x), randint(*safe_area_y))
    
    def hit_seal(self, instance, touch):
        if instance.collide_point(*touch.pos):
            self.score += 1  # Increase score
            self.score_label.text = f"Score: {self.score}"  # Update score label
            self.remove_widget(instance)  # Remove seal from screen
            self.seals.remove(instance)  # Remove seal from list
            self.spawn_seal()  # Spawn a new seal
            return True
        return False

class EndScreen(Screen):
    pass

class CustomButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.click_sound = SoundLoader.load('clicksound.mp3')

    def on_press(self):
        if self.click_sound and App.get_running_app().effects_enabled:  
            self.click_sound.play()  # play sound when press
        return super().on_press()

class HitTheSealApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sound_enabled = True  # Set default value
        self.effects_enabled = True  

    def build(self):
        Builder.load_file('hit_the_seal.kv')
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(RulesGameScreen(name='rules'))
        sm.add_widget(LevelScreen(name='choose_level'))
        sm.add_widget(GameScreen(name='game'))
        sm.add_widget(EndScreen(name='end'))
        return sm
    
    def delayed_switch_to_rules(self, dt):
        self.root.current = 'rules'

    def delayed_exit(self, dt):
        self.stop()
    
    def toggle_sound(self, button):
        self.sound_enabled = not self.sound_enabled
        if self.sound_enabled:
            if self.root.current_screen.background_music:
                self.root.current_screen.background_music.play()
            button.text = "ON"
        else:
            if self.root.current_screen.background_music:
                self.root.current_screen.background_music.stop()
            button.text = "OFF"
        print(f"Sound enabled: {self.sound_enabled}")

    def toggle_effects(self, button):
        self.effects_enabled = not self.effects_enabled
        if self.effects_enabled:
            self.click_sound_enabled = True  # Enable click sound when effects are enabled
            button.text = "ON"
        else:
            self.click_sound_enabled = False  # Disable click sound when effects are disabled
            button.text = "OFF"
        button.text = "ON" if self.effects_enabled else "OFF"
        print(f"Effects enabled: {self.effects_enabled}")
        print(f"Click sound enabled: {self.click_sound_enabled}")

    def show_settings_popup(self):
        popup_content = FloatLayout()
        sound_label = Label(
            text="Sound",
            size_hint=(0.4, 0.1),
            pos_hint={"x": 0.1, "y": 0.6},
            font_size=20,
        )
        effects_label = Label(
            text="Effect",
            size_hint=(0.4, 0.1),
            pos_hint={"x": 0.1, "y": 0.4},
            font_size=20,
        )
        sound_toggle = Button(
            text="ON" if self.sound_enabled else "OFF",
            size_hint=(0.2, 0.1),
            pos_hint={"x": 0.7, "y": 0.6},
            on_press=lambda x: self.toggle_sound(sound_toggle),
        )
        effects_toggle = Button(
            text="ON" if self.effects_enabled else "OFF",
            size_hint=(0.2, 0.1),
            pos_hint={"x": 0.7, "y": 0.4},
            on_press=lambda x: self.toggle_effects(effects_toggle),
        )
        close_button = Button(
            text="Close",
            size_hint=(0.4, 0.1),
            pos_hint={"center_x": 0.5, "y": 0.1},
            on_press=lambda x: settings_popup.dismiss(),
        )

        popup_content.add_widget(sound_label)
        popup_content.add_widget(effects_label)
        popup_content.add_widget(sound_toggle)
        popup_content.add_widget(effects_toggle)
        popup_content.add_widget(close_button)

        settings_popup = Popup(
            title="Setting",
            content=popup_content,
            size_hint=(0.8, 0.5),
            auto_dismiss=False,
        )
        settings_popup.open()
    
    def play_again(self):
        #add delay 0.5 sec before change screeen
        Clock.schedule_once(self.switch_to_level_screen, 0.5)

    def switch_to_level_screen(self, dt):
        self.root.current = 'choose_level'

    def back_to_main(self):
        #add delay 0.5 sec before go back to main 
        Clock.schedule_once(self.switch_to_main, 0.5)

    def switch_to_main(self, dt):
        self.root.current = 'main'

if __name__ == '__main__':
    HitTheSealApp().run()