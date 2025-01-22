from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.floatlayout import FloatLayout
from kivy.core.audio import SoundLoader
from kivy.uix.button import Button
from kivy.graphics import Rectangle
from kivy.storage.jsonstore import JsonStore
from datetime import datetime
from kivy.uix.gridlayout import GridLayout
from kivy.core.audio import SoundLoader

store = JsonStore('user_data.json')

class ImageButton(ButtonBehavior, Image):
    pass

class RegisterScreen(Screen):
    def goto_login(self, instance, touch):
        if instance.collide_point(*touch.pos):
            self.manager.current = 'login'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.clear_widgets()

        # Set background image
        with self.canvas:
            self.bg = Rectangle(source='asset/login.png', size=self.size, pos=self.pos)
        self.bind(size=self.update_bg, pos=self.update_bg)

        # Main layout
        layout = FloatLayout()

        # Form background
        form_bg = Image(source='asset/background.png', size_hint=(0.8, 0.6), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        layout.add_widget(form_bg)

        # Form content layout
        form_layout = BoxLayout(
            orientation="vertical",
            spacing=5,
            size_hint=(None, None),
            width=220,  # Fixed width for alignment
            height=300,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )

        # Register Label
        Register_Label = Label(
            text="Daftar",
            color=(1, 1, 1, 1),
            font_size=20,
            halign="center",
            valign="middle",
            size_hint=(None, None),
            size=(220, 30),
        )
        Register_Label.bind(size=Register_Label.setter('text_size'))
        form_layout.add_widget(Register_Label)

        # Username label and input
        username_label = Label(
            text="NAMA",
            color=(1, 1, 1, 1),
            font_size=15,
            halign="center",
            valign="middle",
            size_hint=(None, None),
            size=(220, 30),
        )
        username_label.bind(size=username_label.setter('text_size'))
        form_layout.add_widget(username_label)

        self.username_input = TextInput(
            multiline=False,
            size_hint=(None, None),
            width=220,
            height=50,
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1),
            hint_text="Masukkan Nama",
            hint_text_color=(0.7, 0.7, 0.7, 1),
        )
        form_layout.add_widget(self.username_input)

        # Password label and input
        password_label = Label(
            text="PASSWORD",
            color=(1, 1, 1, 1),
            font_size=15,
            halign="center",
            valign="middle",
            size_hint=(None, None),
            size=(220, 30),
        )
        password_label.bind(size=password_label.setter('text_size'))
        form_layout.add_widget(password_label)

        self.password_input = TextInput(
            multiline=False,
            password=True,
            size_hint=(None, None),
            width=220,
            height=50,
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1),
            hint_text="Masukkan Password",
            hint_text_color=(0.7, 0.7, 0.7, 1),
        )
        form_layout.add_widget(self.password_input)

        link_layout = GridLayout(cols=2, spacing=10, size_hint=(1, None), height=30)

        login_link = Label(
            text="[u][color=#FFFFFF]Sudah punya akun? Masuk[/color][/u]",
            markup=True,
            font_size=15,
            size_hint=(0.5, 1),
            halign="left",
        )
        login_link.bind(on_touch_down=self.goto_login)
        link_layout.add_widget(login_link)
        form_layout.add_widget(link_layout)

        # Login button with sound effect
        login_button = Button(
            text="MASUK",
            font_size=20,
            background_normal="asset/button.png",
            background_down="asset/button.png",
            size_hint=(None, None),
            size=(220, 50),
            pos_hint={"center_x": 0.5},
            color=(1, 1, 1, 1),  # White text
        )
        login_button.bind(on_press=self.play_sound_and_register)  # Bind to the new method
        form_layout.add_widget(login_button)

        layout.add_widget(form_layout)
        self.add_widget(layout)

    def play_sound_and_register(self, instance):
        # Play the button click sound
        sound = SoundLoader.load('asset/musik/masuk.mp3')
        if sound:
            sound.play()
        
        # Perform the registration logic
        self.register(instance)

    def update_bg(self, *args):
        self.bg.size = self.size
        self.bg.pos = self.pos

    def register(self, instance):
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()

        if username and password:
            created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            store.put('user',
                        name=username,
                        password=password,
                        created_at=created_at,
                        logged_in=True)
            print("Registration successful!")
            self.manager.current = 'game'
        else:
            print("Username and password cannot be empty.")

class LoginScreen(Screen):
    def goto_register(self, instance, touch):
        if instance.collide_point(*touch.pos):
            self.manager.current = 'register'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_ui()

    def setup_ui(self):
        self.clear_widgets()

        with self.canvas.before:
            self.bg = Rectangle(source='asset/login.png', size=self.size, pos=self.pos)
        self.bind(size=self.update_bg, pos=self.update_bg)

        layout = FloatLayout()

        form_bg = Image(source='asset/background.png', size_hint=(0.8, 0.6), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        layout.add_widget(form_bg)

        form_layout = BoxLayout(
            orientation="vertical",
            spacing=5,
            size_hint=(None, None),
            width=220,
            height=300,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )

        login_label = Label(
            text="MASUK", color=(1, 1, 1, 1), font_size=20, halign="center", valign="middle"
        )
        login_label.bind(size=login_label.setter('text_size'))
        form_layout.add_widget(login_label)

        username_label = Label(
            text="NAMA", color=(1, 1, 1, 1), font_size=15, halign="center", valign="middle"
        )
        username_label.bind(size=username_label.setter('text_size'))
        form_layout.add_widget(username_label)

        self.username_input = TextInput(
            multiline=False,
            hint_text="Masukkan Nama",
            size_hint=(None, None),
            width=220,
            height=50,
        )
        form_layout.add_widget(self.username_input)

        password_label = Label(
            text="PASSWORD", color=(1, 1, 1, 1), font_size=15, halign="center", valign="middle"
        )
        password_label.bind(size=password_label.setter('text_size'))
        form_layout.add_widget(password_label)

        self.password_input = TextInput(
            multiline=False,
            password=True,
            hint_text="Masukkan Password",
            size_hint=(None, None),
            width=220,
            height=50,
        )
        form_layout.add_widget(self.password_input)

        link_layout = GridLayout(cols=2, spacing=10, size_hint=(1, None), height=30)
        register_link = Label(
            text="[u][color=#FFFFFF]Belum punya akun? Daftar[/color][/u]",
            markup=True,
            font_size=15,
            size_hint=(0.5, 1),
            halign="right",
        )
        register_link.bind(on_touch_down=self.goto_register)

        link_layout.add_widget(register_link)
        form_layout.add_widget(link_layout)

        # Login button with sound effect
        login_button = Button(
            text="MASUK",
            font_size=20,
            background_normal="asset/button.png",
            background_down="asset/button.png",
            size_hint=(None, None),
            size=(220, 50),
            pos_hint={"center_x": 0.5},
            color=(1, 1, 1, 1),
        )
        login_button.bind(on_press=self.play_sound_and_login)  # Bind to the new method
        form_layout.add_widget(login_button)

        layout.add_widget(form_layout)
        self.add_widget(layout)

    def update_bg(self, *args):
        self.bg.size = self.size
        self.bg.pos = self.pos

    def play_sound_and_login(self, instance):
        # Play the button click sound
        sound = SoundLoader.load('asset/musik/masuk.mp3')
        if sound:
            sound.play()

        # Perform the login logic
        self.login(instance)

    def login(self, instance):
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()

        if store.exists('user'):
            user_data = store.get('user')
            if username == user_data.get('name') and password == user_data.get('password'):
                print("Login successful!")
                self.manager.current = 'game'
            else:
                print("Invalid credentials.")
        else:
            print("No user data found. Please register first.")