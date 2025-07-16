from textual.app import App
from textual.widgets import Static, Label
from rich.markup import escape
from rich.text import Text
from getSearchPatients import get_patient_from_server

class PatientAndIdApp(App):
    def __init__(self, patient, **kwargs):
        super().__init__(**kwargs)
        self.patient = patient

    def compose(self):
        # Create a Static widget and update it with escaped patient name wrapped in a Rich Text object.
        self.static = Static()
        # Escape any characters that might be misinterpreted as markup
        patient_name = self.patient.name[0].given[0] + " " + self.patient.name[0].family
        patient_name_str = escape(str(patient_name))
        # Create a Text object from the escaped string
        patient_text = Text(f"Patient Name: {patient_name_str}")
        self.static.update(patient_text)
        yield self.static

        # Create a Label widget similarly for the patient id.
        self.label = Label()
        patient_id_str = escape(str(self.patient.id))
        patient_id_text = Text(f"Patient ID: {patient_id_str}")
        self.label.update(patient_id_text)
        yield self.label
    
    def on_mount(self):
        # Styling the static
        self.static.styles.background = "blue"
        self.static.styles.border = ("solid", "white")
        self.static.styles.text_align = "center"
        self.static.styles.padding = 1, 1
        self.static.styles.margin = 4, 4
        # Styling the label
        self.label.styles.background = "darkgreen"
        self.label.styles.border = ("double", "red")
        self.label.styles.padding = 1, 1
        self.label.styles.margin = 2, 4



if __name__ == "__main__":
    pt = get_patient_from_server("2")
    app = PatientAndIdApp(pt)
    app.run()
