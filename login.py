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


class ImageButton(ButtonBehavior, Image):
    pass


class LoginScreen(Screen):
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
            spacing=10,
            size_hint=(None, None),
            width=220,  # Fixed width for alignment
            height=300,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )

        # Username label and input
        username_label = Label(
            text="NAMA",
            color=(1, 1, 1, 1),
            font_size=20,
            halign="center",  # Center-align horizontally
            valign="middle",  # Center-align vertically
            size_hint=(None, None),
            size=(220, 50),  # Set the size of the label
        )
        username_label.bind(size=username_label.setter('text_size'))  # Ensure alignment works within bounds
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
            font_size=20,
            halign="center",  # Center-align horizontally
            valign="middle",  # Center-align vertically
            size_hint=(None, None),
            size=(220, 50),  # Set the size of the label
        )
        password_label.bind(size=password_label.setter('text_size'))  # Ensure alignment works within bounds
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

        # Login button
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
        login_button.bind(on_press=self.login)
        form_layout.add_widget(login_button)

        layout.add_widget(form_layout)
        self.add_widget(layout)

    def update_bg(self, *args):
        self.bg.size = self.size
        self.bg.pos = self.pos

    def login(self, instance):
        username = self.username_input.text
        password = self.password_input.text

        if username == "admin" and password == "admin":
            self.manager.current = "game"
        else:
            print("Username atau password salah.")


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        layout.add_widget(Label(text='Selamat Datang di Halaman Home!', font_size=24, size_hint=(1, 0.2)))

        logout_button = Button(text='Logout', size_hint=(None, None), size=(150, 50), pos_hint={'center_x': 0.5})
        logout_button.bind(on_press=self.logout)
        layout.add_widget(logout_button)

        self.add_widget(layout)

    def logout(self, instance):
        self.manager.current = 'login'