import os
os.environ['KIVY_WINDOW_BACKEND'] = 'sdl2'

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from random import sample, choice

RAINBOW_COLORS = [
    (0.2, 0.8, 1, 1),
    (0.2, 1, 0.6, 1),
    (1, 1, 0.2, 1),
    (1, 0.6, 0.2, 1),
    (1, 0.3, 0.7, 1),
    (0.8, 0.2, 1, 1),
]

class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        title = Label(text='LOTO ROMÂNIA', font_size='50sp', color=(1, 0.6, 1, 1), bold=True)
        layout.add_widget(title)
        
        subtitle = Label(text='Alege jocul', font_size='30sp', color=(0.8, 0.8, 1, 1))
        layout.add_widget(subtitle)
        
        btn_5_40 = Button(text='5 din 40', font_size='35sp', size_hint_y=None, height=100, background_color=(0.1, 0.6, 1, 1))
        btn_5_40.bind(on_press=lambda x: app.show_game('5/40', 5, 40))
        layout.add_widget(btn_5_40)
        
        btn_joker = Button(text='JOKER (5 + 1)', font_size='35sp', size_hint_y=None, height=100, background_color=(1, 0.7, 0, 1))
        btn_joker.bind(on_press=lambda x: app.show_game('JOKER', 5, 45, extra=1))
        layout.add_widget(btn_joker)
        
        btn_6_49 = Button(text='6 din 49', font_size='35sp', size_hint_y=None, height=100, background_color=(0.8, 0.2, 0.8, 1))
        btn_6_49.bind(on_press=lambda x: app.show_game('6/49', 6, 49))
        layout.add_widget(btn_6_49)
        
        self.add_widget(layout)

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game_layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        self.add_widget(self.game_layout)
    
    def load_game(self, name, count, max_num, extra=0):
        self.game_layout.clear_widgets()
        
        game_title = Label(text=name, font_size='50sp', color=(1, 0.8, 0, 1), bold=True)
        self.game_layout.add_widget(game_title)
        
        numbers_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=120, spacing=15)
        self.number_labels = []
        for i in range(count):
            lbl = Label(text='?', font_size='50sp', color=RAINBOW_COLORS[i % len(RAINBOW_COLORS)], bold=True)
            numbers_layout.add_widget(lbl)
            self.number_labels.append(lbl)
        self.game_layout.add_widget(numbers_layout)
        
        self.extra_label = None
        if extra:
            extra_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=100, spacing=20)
            extra_layout.add_widget(Label(text='+ Joker:', font_size='40sp', color=(1, 1, 0, 1)))
            extra_lbl = Label(text='?', font_size='50sp', color=(1, 1, 0, 1), bold=True)
            extra_layout.add_widget(extra_lbl)
            self.extra_label = extra_lbl
            self.game_layout.add_widget(extra_layout)
        
        generate_btn = Button(text='GENEREAZĂ', font_size='40sp', size_hint_y=None, height=100, background_color=(0, 0.8, 0.4, 1))
        generate_btn.bind(on_press=lambda x: app.generate(name, count, max_num, extra))
        self.game_layout.add_widget(generate_btn)
        
        self.lucky_label = Label(text='Apasă și scrie istorie!', font_size='28sp', color=(1, 1, 0, 1))
        self.game_layout.add_widget(self.lucky_label)
        
        history_title = Label(text='Istoric:', font_size='30sp', color=(1, 1, 1, 1))
        self.game_layout.add_widget(history_title)
        
        scroll = ScrollView(size_hint_y=0.4)
        self.history_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
        self.history_layout.bind(minimum_height=self.history_layout.setter('height'))
        scroll.add_widget(self.history_layout)
        self.game_layout.add_widget(scroll)
        
        back_btn = Button(text='ÎNAPOI LA MENIU', font_size='28sp', size_hint_y=None, height=80, background_color=(0.6, 0.6, 0.6, 1))
        back_btn.bind(on_press=lambda x: setattr(sm, 'current', 'menu'))
        self.game_layout.add_widget(back_btn)

class LotoApp(App):
    def build(self):
        global sm, app
        app = self
        Window.clearcolor = (0.05, 0.02, 0.1, 1)
        
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(GameScreen(name='game'))
        
        return sm
    
    def show_game(self, name, count, max_num, extra=0):
        sm.get_screen('game').load_game(name, count, max_num, extra)
        sm.current = 'game'
    
    def generate(self, name, count, max_num, extra=0):
        numbers = sorted(sample(range(1, max_num + 1), count))
        extra_num = sample(range(1, 21), 1)[0] if extra else None
        
        game_screen = sm.get_screen('game')
        for i, lbl in enumerate(game_screen.number_labels):
            lbl.text = str(numbers[i])
            lbl.color = RAINBOW_COLORS[i % len(RAINBOW_COLORS)]
        
        if game_screen.extra_label:
            game_screen.extra_label.text = str(extra_num)
        
        messages = [
            "Noroc chior azi!",
            "Simt că vine câștigul mare!",
            "Numerele câștigătoare!",
            "Stelele îți zâmbesc!",
            "Hai că azi e ziua ta!",
            "Azi sigur câștigi!",
            "Totul se întâmplă acum!",
            "Nimeni nu te poate opri!",
            "E ziua ta norocoasă!",
            "Hristos, e cu tine!",
            "Totul se va schimba acum!",
        ]
        game_screen.lucky_label.text = choice(messages)
        
        text = ' '.join(f'{n:02d}' for n in numbers)
        if extra_num:
            text += f' + {extra_num:02d}'
        history_lbl = Label(text=text, font_size='32sp', color=(1, 1, 0.8, 1), size_hint_y=None, height=70)
        game_screen.history_layout.add_widget(history_lbl)
        
        if len(game_screen.history_layout.children) > 8:
            game_screen.history_layout.remove_widget(game_screen.history_layout.children[-1])

LotoApp().run()