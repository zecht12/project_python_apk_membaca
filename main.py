from kivy.config import Config

# Set the resolution and prevent resizing
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')
Config.set('graphics', 'resizable', False)

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from game import MainScreen, Level1Screen, Level2Screen, Level3Screen

# Subclass ImageButton for image-based buttons
class ImageButton(ButtonBehavior, Image):
    pass

# Main menu screen
class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        
        # Background image
        background = Image(
            source='asset/back1.png',
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
            pos_hint={'x': 0, 'y': 0}
        )
        layout.add_widget(background)

        # Title of the game
        title_label = Label(
            text="BELAJAR MEMBACA",
            font_size='60sp',
            size_hint=(None, None),
            size=(500, 100),
            color=(1, 1, 1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )
        layout.add_widget(title_label)

        # Start button
        start_button = ImageButton(
            source='asset/anakpanah.png',  # Replace with your button image
            size_hint=(None, None),
            size=(150, 150),
            pos_hint={'center_x': 0.5, 'center_y': 0.4}
        )
        start_button.bind(on_press=self.go_to_login)
        layout.add_widget(start_button)

        self.add_widget(layout)

    def go_to_login(self, instance):
        self.manager.current = 'login'

class MainApp(App):
    def build(self):
        screen_manager = ScreenManager(transition=WipeTransition())
        
        # Add screens
        screen_manager.add_widget(MainMenuScreen(name='main'))
        
        try:
            from login import LoginScreen
            screen_manager.add_widget(LoginScreen(name='login'))
        except ImportError as e:
            print(f"Error importing LoginScreen: {e}")
            placeholder = Screen(name='login')
            placeholder.add_widget(Label(text="Login screen not found!", font_size='24sp', pos_hint={'center_x': 0.5, 'center_y': 0.5}))
            screen_manager.add_widget(placeholder)

        # Add game screen
        game_screen = Screen(name='game')
        game_screen.add_widget(MainScreen())
        screen_manager.add_widget(game_screen)
        screen_manager.add_widget(Level1Screen(name="level1"))
        screen_manager.add_widget(Level2Screen(name="level2"))
        screen_manager.add_widget(Level3Screen(name="level3"))

        return screen_manager

if __name__ == "__main__":
    MainApp().run()
