import textual
from textual import on
from textual.app import App
from textual.command import Button, Input
from textual.widgets import Label


class FormApp(App):
    def compose(self):
        yield Input(placeholder="Type your name here...")
        yield Button("Submit your name")
    
    @on(Button.Pressed)
    @on(Input.Submitted)
    def accept_user_name(self):
        input = self.query_one(Input)
        user_name = input.value
        self.mount(Label(user_name))
        input.value = ""
        
        
if __name__ == '__main__':
    app = FormApp()
    app.run() 
