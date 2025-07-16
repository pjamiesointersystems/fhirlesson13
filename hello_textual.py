from textual.app import App
from textual.widgets import Static


class HelloTextualApp(App):
    
    BINDINGS = [("ctrl+q", "quit", "Quit Application")]
    
    def compose(self):
        ## What widgets is the app composed of?
        yield Static("Hello, Textual")
        
        

    async def action_quit(self) -> None:
        # This will shut down the app.
          self.exit()





if __name__ == "__main__":
   app = HelloTextualApp()
   app.run()