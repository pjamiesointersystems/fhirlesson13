from textual.app import App, ComposeResult
from textual.widgets import TabbedContent, Tabs, Tab, TabPane, DataTable, Label

class TabbedDemoApp(App):

    def compose(self) -> ComposeResult:
        with TabbedContent():
            yield Tabs(
                Tab("Patients", id="patients-tab"),
                Tab("Observations", id="obs-tab")
            )
            with TabPane("Patients", id="patients-tab"):
                yield Label("This is the Patient View")
                yield DataTable(zebra_stripes=True)
            with TabPane("Observations", id="obs-tab"):
                yield Label("This is the Observation View")
                yield DataTable(zebra_stripes=True)

if __name__ == "__main__":
    app = TabbedDemoApp()
    app.run()
