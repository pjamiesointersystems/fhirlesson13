from textual.app import App
from textual.widgets import Footer
from textual.widgets import Input, Static
from textual import events
from textual import on
from textual.containers import HorizontalScroll
from rich.markup import escape
from rich.text import Text
from fhir.resources.patient import Patient
from getSearchPatients import get_patient_from_server

class FHIRPatientApp(App):
    CSS_PATH = "events.tcss"
    BINDINGS = [
        ("enter", "fetch_patient", "Fetch Patient"),
        ("q", "quit", "Quit"),
    ]

    def compose(self):
    # Input widget for entering the patient id
     self.patient_input = Input(placeholder="Enter Patient ID", id="patient_input")
     yield self.patient_input

        # Display area for patient details
     self.patient_display = Static(id="patient_display")
     yield self.patient_display
     
     def action_fetch_patient(self):
        # Get the text from the Input widget
        patient_id = self.query_one("#patient_input").value

        # Retrieve the patient using your function (assumed to be defined)
        patient = get_patient_from_server(patient_id)

        # Update the display widget with patient details.
        # Assume the patient object can be converted to a string for display.
        self.patient_display.update(str(patient))

    

if __name__ == "__main__":
    app = EventsApp()
    app.run()