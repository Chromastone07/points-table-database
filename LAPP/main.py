from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp

KV = '''
ScreenManager:
    MainScreen:

<MainScreen>:
    name: "main"
    BoxLayout:
        orientation: "vertical"
        spacing: dp(20)
        padding: dp(20)

        MDLabel:
            text: "Enter your choice (1-3):"
            halign: "center"

        MDTextField:
            id: user_input
            hint_text: "Type your choice here"
            input_filter: "int"
            helper_text: "Choose between 1, 2, or anything else"
            helper_text_mode: "on_focus"
        
        MDRaisedButton:
            text: "Submit"
            pos_hint: {"center_x": 0.5}
            on_release: app.process_choice()

        MDLabel:
            id: result_label
            text: ""
            halign: "center"
'''

class MainScreen(Screen):
    pass

class RomanticApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def process_choice(self):
        user_input = self.root.get_screen("main").ids.user_input.text
        result_label = self.root.get_screen("main").ids.result_label

        if user_input == "1":
            result_label.text = "She's an idiot. 😅"
        elif user_input == "2":
            result_label.text = "She's smart. 😊"
        else:
            result_label.text = "She's extraordinary! ❤️"

if __name__ == "__main__":
    RomanticApp().run()
