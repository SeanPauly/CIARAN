from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.list import OneLineListItem
from kivy.uix.scrollview import ScrollView

# You can replace this simple echo bot with a more sophisticated one
def get_bot_response(user_input):
    return f"You said: {user_input}"


class ChatApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.title = "Simple KivyMD Chatbot"

        # Load the KV file (Kivy language)
        self.root = Builder.load_string(
            '''
BoxLayout:
    orientation: 'vertical'

    ScrollView:
        id: scroll_view

        MDList:
            id: chat_container

    BoxLayout:
        size_hint_y: None
        height: "48dp"

        MDTextField:
            id: user_input
            hint_text: "Enter message"
            on_text_validate: app.send_message()
            
        MDIconButton:
            icon: "send"
            on_release: app.send_message()
        '''
        )
        return self.root

    def send_message(self):
        user_input = self.root.ids.user_input.text

        if user_input.strip() != "":
            # Display user message in the chat interface
            user_message = OneLineListItem(text=user_input, align="right")
            self.root.ids.chat_container.add_widget(user_message)

            # Get bot's response and display it in the chat interface
            bot_response = get_bot_response(user_input)
            bot_message = OneLineListItem(text=bot_response, align="left")
            self.root.ids.chat_container.add_widget(bot_message)

            # Clear the user input field
            self.root.ids.user_input.text = ""

            # Scroll to the bottom of the chat interface
            self.root.ids.scroll_view.scroll_y = 0

if __name__ == '__main__':
    ChatApp().run()
