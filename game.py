import pyttsx3
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
import random
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

        # Add "Mulai" button with text and sound
        self.start_button = Button(
            text="[color=ffffff][b]MULAI[/b][/color]",
            markup=True,
            halign='center',
            valign='middle',
            background_normal='asset/button_mulai.png',
            size_hint=(0.15, 0.05),
            pos_hint={'center_x': 0.5, 'center_y': 0.45},
        )

        def play_entry_sound_and_start_level(instance):
            # Play the entry sound
            sound = SoundLoader.load('asset/musik/entry.mp3')
            if sound:
                sound.play()
            # Proceed to the selected level
            self.start_level(instance)

        # Bind the button press to play sound and navigate to the level
        self.start_button.bind(on_press=play_entry_sound_and_start_level)
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

            # Define the on_press callback with sound playback
            def on_button_press(instance, l=level['level']):
                # Play the masuk sound
                sound = SoundLoader.load('asset/musik/masuk.mp3')
                if sound:
                    sound.play()
                # Call select_level
                self.select_level(l)

            # Bind the button to the custom callback
            btn.bind(on_press=on_button_press)
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
        button_size = 0.1  # Size of each button
        gap = 0.02  # Gap between buttons
        columns = 6  # Number of buttons per row

        for i, letter in enumerate(letters):
            # Calculate x and y positions dynamically based on the index
            x_pos = (i % columns) * (button_size + gap) + (1 - columns * button_size - (columns - 1) * gap) / 2
            y_pos = 0.7 - (i // columns) * (button_size + gap)

            btn = Button(
                text=letter,
                background_normal='asset/button_jawab.png',
                size_hint=(button_size, button_size),
                pos_hint={
                    'x': x_pos,
                    'y': y_pos,
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

        # Define the on_press callback with sound playback
        def on_exit_press(instance):
            # Play the keluar sound
            sound = SoundLoader.load('asset/musik/keluar.mp3')
            if sound:
                sound.play()
            # Navigate to the main screen
            self.exit_to_main()

        # Bind the button to the custom callback
        exit_btn.bind(on_press=on_exit_press)
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

        # Define the on_press callback with sound playback
        def on_exit_press(instance):
            # Play the keluar sound
            sound = SoundLoader.load('asset/musik/keluar.mp3')
            if sound:
                sound.play()
            # Navigate to the main screen
            self.exit_to_main()

        # Bind the button to the custom callback
        exit_btn.bind(on_press=on_exit_press)
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
CORRECT_ANSWER = [word.lower() for word in kata_benda + kata_kerja]  # Normalize to lowercase

class Level3Screen(Screen):
    def exit_to_main(self):
        App.get_running_app().root.current = "game"
    def __init__(self, **kwargs):
        super(Level3Screen, self).__init__(**kwargs)
        self.score = 0
        self.current_question = 0
        self.total_questions = 4
        self.time_left = 20
        self.current_word = ""
        self.timer_event = None

        layout = FloatLayout()

        # Set white background
        self.background = Image(source='asset/level3.jpeg', allow_stretch=True, keep_ratio=False, color=[1, 1, 1, 1])
        self.add_widget(self.background)

        # Add "DENGARKAN BAIK-BAIK" text
        title = Label(
            text="[b]DENGARKAN BAIK-BAIK[/b]",
            markup=True,
            font_size="24sp",
            color=(0, 0, 0, 1),
            pos_hint={"center_x": 0.5, "y": 0.3},
        )
        layout.add_widget(title)

        # Add timer label
        self.timer_label = Label(
            text=f"Waktu: {self.time_left} detik",
            font_size="18sp",
            color=(0, 0, 0, 1),
            pos_hint={"center_x": 0.5, "y": 0.2},
        )
        layout.add_widget(self.timer_label)

        # Add input field
        self.input_field = TextInput(
            hint_text="Masukkan jawaban...",
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
            pos_hint={"center_x": 0.5, "y": 0.2},
        )
        send_btn.bind(on_press=self.submit_answer)
        layout.add_widget(send_btn)

        self.add_widget(layout)
        self.start_question()

    def start_question(self):
        # Reset input and timer
        self.input_field.text = ""
        self.time_left = 20
        self.update_timer_label()

        # Select a random word and play audio
        self.current_word = random.choice(kata_benda + kata_kerja).lower()
        sound_path = f"asset/musik/{self.current_word}.mp3"
        sound = SoundLoader.load(sound_path)
        if sound:
            sound.play()

        # Start timer
        if self.timer_event:
            self.timer_event.cancel()
        self.timer_event = Clock.schedule_interval(self.update_timer, 1)

    def update_timer(self, dt):
        self.time_left -= 1
        self.update_timer_label()

        if self.time_left <= 0:
            self.timer_event.cancel()
            self.show_popup("Waktu Habis!", "Jawaban yang benar: " + self.current_word)

    def update_timer_label(self):
        self.timer_label.text = f"Waktu: {self.time_left} detik"

    def submit_answer(self, instance):
        user_answer = self.input_field.text.strip().lower()
        if user_answer == self.current_word:
            self.score += 25
            self.show_popup("Benar!", "Jawaban Anda benar.")
        else:
            self.show_popup("Salah!", "Jawaban Anda salah.")

    def show_popup(self, title, message):
        content = FloatLayout()

        label = Label(
            text=message,
            font_size="18sp",
            halign="center",
            valign="middle",
            color=(0, 0, 0, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.6},
        )
        content.add_widget(label)

        next_btn = Button(
            text="[color=ffffff]LANJUT[/color]",
            markup=True,
            background_normal='asset/button_keluar.png',
            size_hint=(0.4, 0.3),
            pos_hint={'center_x': 0.5, 'y': 0.1},
        )
        next_btn.bind(on_press=lambda x: self.next_question())
        content.add_widget(next_btn)

        self.popup = Popup(
            title=title,
            content=content,
            separator_color=(0, 0, 0, 0),
            background="asset/white.png",
            size_hint=(0.8, 0.5),
            auto_dismiss=False,
        )
        self.popup.open()

    def next_question(self):
        if self.popup:
            self.popup.dismiss()
            self.popup = None

        self.current_question += 1
        if self.current_question < self.total_questions:
            self.start_question()
        else:
            self.show_final_score()

    def show_final_score(self):
        content = FloatLayout()

        label = Label(
            text=f"Skor Akhir Anda: {self.score}",
            font_size="20sp",
            halign="center",
            valign="middle",
            color=(0, 0, 0, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.6},
        )
        content.add_widget(label)

        exit_btn = Button(
            text="[color=ffffff]KELUAR[/color]",
            markup=True,
            background_normal='asset/button_keluar.png',
            size_hint=(0.4, 0.3),
            pos_hint={'center_x': 0.5, 'y': 0.1},
        )

        def exit_to_main(instance):
            self.exit_to_main()
            popup.dismiss()

        exit_btn.bind(on_press=exit_to_main)
        content.add_widget(exit_btn)

        popup = Popup(
            title="Game Selesai",
            content=content,
            separator_color=(0, 0, 0, 0),
            background="asset/white.png",
            size_hint=(0.8, 0.5),
            auto_dismiss=False,
        )
        popup.open()
