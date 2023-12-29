from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.label import MDLabel
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivymd.uix.list import TwoLineListItem

from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout

kv = '''
ScreenManager:
    MainScreen:

<MainScreen>:
    name: 'main'
    
    BoxLayout:
        orientation: 'horizontal'
        spacing: dp(10)
        padding: dp(0)
        canvas.before:
            Color:
                rgba: .18, .18, .18, 1                
            Rectangle:
                size: self.size
                pos: self.pos

        BoxLayout:
            id: info
            orientation: 'vertical'
            size_hint_y: 1
            size_hint_x: .45 
            padding: '10dp'
            canvas.before:
                Color:
                    rgba: 12/255, 15/255, 23/255, 1  # Adjusted RGBA values for the color
                Rectangle:
                    size: self.size
                    pos: self.pos


            TypingLabel:
                id: title
                text: ''
                font_style: 'H4'
                halign: 'center'
                size_hint_y: None
                height: self.texture_size[1] + dp(10)
                color: 0, 74/255, 173/255, 1  # Font color rgba(0, 74, 173, 1)

            MDLabel:
                text: 'Find inspiration for your work, acquire new knowledge, and receive prompt responses.'
                theme_text_color: 'Custom'  # Use custom text color
                text_color: 0, 74/255, 173/255, 1  # Font color rgba(0, 74, 173, 1)

        BoxLayout:
            orientation: 'vertical'
            size_hint_x: .55
            canvas.before:
                Color:
                    rgba: .18, .18, .18, 1    # Set the RGBA values for the color
                Rectangle:
                    size: self.size
                    pos: self.pos
            ScrollView:
                size_hint: (1, None)
                height: root.height

                GridLayout:
                    id: chat_history
                    cols: 1
                    size_hint_y: None
                    height: self.minimum_height
                    padding: dp(10)
                    spacing: dp(10)

            MDTextField:
                id: input_text
                hint_text: 'Enter input'
                size_hint: None, None
                size: self.parent.width - dp(20), self.minimum_height
                pos_hint: {'center_x': 0.5}
                multiline: False
                on_text_validate: app.calculate_integration()
                pos_hint: {'bottom': 1}
                color_mode: 'custom'  # Set custom text color
                line_color_normal: 0, 74/255, 173/255, 1  # Font color rgba(0, 74, 173, 1)

'''

# Define a custom lABEL for typing animation
class TypingLabel(MDLabel):
    def start_typing(self, text, final_text=None, target_widget=None, delay=0):
        self.typing_text = text
        self.markup = True
        self.final_text = final_text
        self.target_widget = target_widget  # Widget to modify size_hint_x
        self.typing_speed = 0.1
        self.typing_index = 0
        Clock.schedule_once(lambda dt: Clock.schedule_interval(self.update_text, self.typing_speed), delay)

    def update_text(self, dt):
        if self.typing_index <= len(self.typing_text):
            self.text = self.typing_text[:self.typing_index]
            self.typing_index += 1
        else:
            if self.final_text:
                self.text = self.final_text
                if self.target_widget:  # Check if target_widget is provided
                    self.target_widget.size_hint_x = 0.25  # Change size_hint_x of the target_widget
            Clock.unschedule(self.update_text)


# Define a custom ListItemText for typing animation
class TypingList(TwoLineListItem):
    def start_typing(self, text, delay=0):
        self.secondary_text = ''  # Empty the secondary text
        self.typing_text = text
        self.typing_speed = 0.1  # Adjust typing speed (in seconds)
        self.typing_index = 0
        Clock.schedule_once(lambda dt: Clock.schedule_interval(self.update_text, self.typing_speed), delay)

    def update_text(self, dt):
        if self.typing_index <= len(self.typing_text):
            self.secondary_text = self.typing_text[:self.typing_index]
            self.typing_index += 1
        else:
            Clock.unschedule(self.update_text)
# Define screens
class MainScreen(Screen):
    pass

# Create the app
class CIARANApp(MDApp):
    def build(self):
        self.icon = r'./documentation/CIARAN Logo/3.png'
        self.theme_cls.theme_style = "Light"
        self.sm = ScreenManager()
        self.sm.add_widget(MainScreen(name='main'))
        return Builder.load_string(kv)

    # Inside the CIARANApp class, in the on_start method:
    def on_start(self):
        main_screen = self.root.get_screen('main')
        info_boxlayout = main_screen.ids.info  # Get the BoxLayout with id "info"
        main_screen.ids.title.start_typing('Welcome to CIARAN', final_text='[b]CIARAN[/b]', target_widget=info_boxlayout)


    def calculate_integration(self):
        screen = self.root.get_screen('main')
        input_text = screen.ids.input_text.text

        you_message = TwoLineListItem(
            theme_text_color='Custom',
            text_color=(0, 74/255, 173/255, 1),
            secondary_text_color=(0, 74/255, 173/255, 1),
            text=f'[b]You:[/b]',
            secondary_text=f'{input_text}'
        )

        ciaran_message = TypingList(
            theme_text_color='Custom',
            text_color=(0, 74/255, 173/255, 1),
            secondary_text_color=(0, 74/255, 173/255, 1),
            text=f'[b]CIARAN:[/b]',
            secondary_text=f'This is the result for the input [b]"{input_text}"[/b]'
        )

        # Add new messages to the chat history GridLayout
        screen.ids.chat_history.add_widget(you_message)
        # Start typing animation for the secondary text of ciaran_message
        ciaran_message.start_typing(f'This is the result for the input [b]"{input_text}"[/b]', delay=0.5)
        screen.ids.chat_history.add_widget(ciaran_message)
        screen.ids.input_text.text = ""  # Clear input after calculation

        # Scroll to the bottom after adding messages
        Clock.schedule_once(lambda dt: self.scroll_to_bottom(screen.ids.chat_history))

    def scroll_to_bottom(self, widget):
        widget.parent.scroll_y = 0
# Run the app
if __name__ == '__main__':
    CIARANApp().run()
