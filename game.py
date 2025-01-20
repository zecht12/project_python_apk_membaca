import pyttsx3
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivy.core.audio import SoundLoader
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput

# Initialize pyttsx3 for text-to-speech
engine = pyttsx3.init()


def speak(text):
    engine.say(text)
    engine.runAndWait()

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.setup_ui()
        self.selected_level = None

        # Play background music
        self.sound = SoundLoader.load('asset/musik/homepage.mp3')
        if self.sound:
            self.sound.loop = True
            self.sound.play()

    def setup_ui(self):
        self.clear_widgets()  # Clear previous widgets if necessary

        # Set background image
        self.background = Image(source='asset/homepage.png', allow_stretch=True, keep_ratio=False)
        self.add_widget(self.background)

        # Add title and description text on the board
        self.title_label = Label(
            text="[color=ffffff][b]PILIH LEVEL[/b][/color]",
            markup=True,
            font_size='20sp',
            halign='center',
            valign='middle',
            pos_hint={'center_x': 0.5, 'center_y': 0.58},
        )
        self.add_widget(self.title_label)

        self.description_label = Label(
            text="[color=ffffff]Silakan pilih level untuk melihat deskripsi.[/color]",
            markup=True,
            halign='center',
            valign='middle',
            font_size='16sp',
            pos_hint={'center_x': 0.5, 'center_y': 0.53},
        )
        self.add_widget(self.description_label)

        # Add "Mulai" button with text
        self.start_button = Button(
            text="[color=ffffff][b]MULAI[/b][/color]",
            markup=True,
            halign='center',
            valign='middle',
            background_normal='asset/button_mulai.png',
            size_hint=(0.15, 0.05),
            pos_hint={'center_x': 0.5, 'center_y': 0.45},
        )
        self.start_button.bind(on_press=self.start_level)
        self.add_widget(self.start_button)

        # Add buttons for Level 1, 2, and 3
        levels = [
            {"image": "asset/level1.png", "text": "LEVEL 1", "pos_hint": {"x": 0.2, "y": 0.2}, "level": 1},
            {"image": "asset/level2.png", "text": "LEVEL 2", "pos_hint": {"x": 0.4, "y": 0.2}, "level": 2},
            {"image": "asset/level3.png", "text": "LEVEL 3", "pos_hint": {"x": 0.6, "y": 0.2}, "level": 3},
        ]

        for level in levels:
            btn = Button(
                text=f"[color=ffffff][b]{level['text']}[/b][/color]",
                markup=True,
                halign="center",
                valign="middle",
                background_normal=level['image'],
                size_hint=(0.15, 0.15),
                pos_hint=level['pos_hint'],
            )
            btn.bind(on_press=lambda instance, l=level['level']: self.select_level(l))
            self.add_widget(btn)

    def select_level(self, level):
        """Update title and description based on the selected level."""
        self.selected_level = level
        if level == 1:
            self.title_label.text = "[color=ffffff][b]LEVEL 1 MENGENAL HURUF[/b][/color]"
            self.description_label.text = "[color=ffffff]Level 1 mengenal huruf\na sampai z[/color]"
        elif level == 2:
            self.title_label.text = "[color=ffffff][b]LEVEL 2[/b][/color]"
            self.description_label.text = "[color=ffffff]Level 2 mengenal huruf vokal AIUEO[/color]"
        elif level == 3:
            self.title_label.text = "[color=ffffff][b]LEVEL 3[/b][/color]"
            self.description_label.text = "[color=ffffff]Level 3 permainan tebak huruf[/color]"

    def start_level(self, instance):
        """Navigate to the selected level screen."""
        if self.selected_level:
            app = App.get_running_app()
            if self.selected_level == 1:
                app.root.current = "level1"
            elif self.selected_level == 2:
                app.root.current = "level2"
            elif self.selected_level == 3:
                app.root.current = "level3"
        else:
            # Show a message if no level is selected
            print("Please select a level before starting.")

class Level1Screen(Screen):
    def exit_to_main(self):
        App.get_running_app().root.current = "game"
    def __init__(self, **kwargs):
        super(Level1Screen, self).__init__(**kwargs)
        layout = FloatLayout()

        # Set white background
        self.background = Image(source='asset/level1.jpeg', allow_stretch=True, keep_ratio=False, color=[1, 1, 1, 1])
        self.add_widget(self.background)

        title = Label(
            text="[b]HURUF A SAMPAI Z[/b]",  # Black text
            markup=True,
            font_size="24sp",
            color=(0,0,0,1),
            pos_hint={"center_x": 0.5, "y": 0.4},
        )
        layout.add_widget(title)

        # Add smaller buttons for letters A-Z
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        button_size = 0.1
        gap = 0.02
        for i, letter in enumerate(letters):
            btn = Button(
                text=letter,
                background_normal='asset/button_jawab.png',
                size_hint=(button_size, button_size),
                pos_hint={
                    'x': (i % 10) * (button_size + gap) + 0.05,
                    'y': 0.7 - (i // 10) * (button_size + gap),
                },
            )
            btn.bind(on_press=lambda instance, l=letter: self.play_audio(l))
            layout.add_widget(btn)

        exit_btn = Button(
            text="[color=ffffff]KELUAR[/color]",
            markup=True,
            background_normal='asset/button_keluar.png',
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.5, 'y': 0.1},
        )
        exit_btn.bind(on_press=lambda instance: self.exit_to_main())
        layout.add_widget(exit_btn)

        self.add_widget(layout)

    def play_audio(self, letter):
        """Play the corresponding letter audio from the assets folder."""
        sound_path = f"asset/musik/{letter.lower()}.mp3"
        sound = SoundLoader.load(sound_path)
        if sound:
            sound.play()
        else:
            print(f"Audio file {sound_path} not found.")

class Level2Screen(Screen):
    def exit_to_main(self):
        App.get_running_app().root.current = "game"
    def __init__(self, **kwargs):
        super(Level2Screen, self).__init__(**kwargs)
        layout = FloatLayout()

        # Set white background
        self.background = Image(source='asset/level2.jpeg', allow_stretch=True, keep_ratio=False, color=[1, 1, 1, 1])
        self.add_widget(self.background)

        title = Label(
            text="[b]HURUF VOKAL AIUEO[/b]",
            markup=True,
            font_size="24sp",
            color=(0,0,0,1),
            pos_hint={"center_x": 0.5, "y": 0.2},
        )
        layout.add_widget(title)

        # Add buttons for vowels A, I, U, E, O
        vowels = "AIUEO"
        button_size = 0.1
        gap = 0.05
        for i, vowel in enumerate(vowels):
            btn = Button(
                text=vowel,
                background_normal='asset/button_jawab1.png',
                size_hint=(0.08, 0.08),
                pos_hint={
                    'x': 0.2 + i * (button_size + gap) - gap,
                    'y': 0.5,
                },
            )
            btn.bind(on_press=lambda instance, v=vowel: self.play_audio(v))
            layout.add_widget(btn)

        exit_btn = Button(
            text="[color=ffffff]KELUAR[/color]",
            markup=True,
            background_normal='asset/button_keluar.png',
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.5, 'y': 0.1},
        )
        exit_btn.bind(on_press=lambda instance: self.exit_to_main())
        layout.add_widget(exit_btn)

        self.add_widget(layout)

    def play_audio(self, vowel):
        """Play the corresponding vowel audio from the assets folder."""
        sound_path = f"asset/musik/{vowel.lower()}.mp3"
        sound = SoundLoader.load(sound_path)
        if sound:
            sound.play()
        else:
            print(f"Audio file {sound_path} not found.")

kata_benda = ["mobil", "pohon", "buku", "kucing", "rumah"]
kata_kerja = ["lari", "makan", "tidur", "baca", "tulis"]

CORRECT_ANSWER = kata_benda + kata_kerja

class Level3Screen(Screen):
    def exit_to_main(self):
        App.get_running_app().root.current = "game"

    def __init__(self, **kwargs):
        super(Level3Screen, self).__init__(**kwargs)
        layout = FloatLayout()

        # Play the audio when the screen is initialized
        self.sound = SoundLoader.load('asset/musik/soal_level3.mp3')
        if self.sound:
            self.sound.play()

        # Set white background
        self.background = Image(source='asset/level3.jpeg', allow_stretch=True, keep_ratio=False, color=[1, 1, 1, 1])
        self.add_widget(self.background)

        # Add "DENGARKAN BAIK-BAIK" text
        title = Label(
            text="[b]DENGARKAN BAIK-BAIK[/b]",
            markup=True,
            font_size="24sp",
            color=(0,0,0,1),
            pos_hint={"center_x": 0.5, "y": 0.2},
        )
        layout.add_widget(title)

        # Add input field
        self.input_field = TextInput(
            hint_text="Masukkan jawaban...",
            background_normal='asset/input.png',
            multiline=False,
            size_hint=(0.6, 0.15),
            pos_hint={"center_x": 0.5, "y": 0.5},
        )
        layout.add_widget(self.input_field)

        # Add "KIRIM" button
        send_btn = Button(
            text="[color=ffffff]KIRIM[/color]",
            markup=True,
            background_normal='asset/button_keluar.png',
            size_hint=(0.3, 0.1),
            pos_hint={"center_x": 0.5, "y": 0.3},
        )
        send_btn.bind(on_press=self.check_answer)
        layout.add_widget(send_btn)

        self.add_widget(layout)

    def check_answer(self, instance):
        user_answer = self.input_field.text.strip()
        if user_answer == CORRECT_ANSWER:
            self.show_popup("Correct!", "Jawaban Anda benar.")
        else:
            self.show_popup("Incorrect!", "Jawaban Anda salah.")

    def show_popup(self, title, message):
        content = FloatLayout()

        # Add message
        label = Label(
            text=message,
            font_size="18sp",
            halign="center",  # Center-align horizontally
            valign="middle",  # Center-align vertically
            color=(0, 0, 0, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.6},
        )
        content.add_widget(label)

        exit_btn = Button(
            text="[color=ffffff]KELUAR[/color]",
            markup=True,
            background_normal='asset/button_keluar.png',
            size_hint=(0.4, 0.2),
            pos_hint={"center_x": 0.5, "center_y": 0.3},
        )

        def dismiss_popup_and_exit(instance):
            popup.dismiss()
            self.exit_to_main()

        exit_btn.bind(on_press=dismiss_popup_and_exit)
        content.add_widget(exit_btn)

        popup = Popup(
            title=title,
            content=content,
            background="asset/white.png",
            size_hint=(0.8, 0.5),
            auto_dismiss=False,
            separator_color=(0, 0, 0, 0),
            title_color=(0,0,0,1),
            title_size=(24),
            title_align="center",
        )
        popup.open()