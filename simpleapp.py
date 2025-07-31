
from textual.app import App, ComposeResult
from textual.widgets import DataTable, Header, Footer
from rich.markup import escape

class SimpleApp(App):
    
    BINDINGS = [('d', 'toggle_dark', 'Toggle dark mode')]
    
    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
    
        
    def action_toggle_dark(self) -> None:
        return super().action_toggle_dark()
        
        
if __name__ == '__main__':
    app = SimpleApp()
    app.run() 