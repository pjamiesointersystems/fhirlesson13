from textual.app import App
from textual.widgets import Static, Label
from rich.markup import escape
from rich.text import Text
from getSearchPatients import get_patient_from_server


class PatientAndIdAppTCSS(App):
    
    CSS_PATH = "static_and_label.tcss"
    
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
        self.label.add_class("patientId")
        patient_id_str = escape(str(self.patient.id))
        patient_id_text = Text(f"Patient ID: {patient_id_str}")
        self.label.update(patient_id_text)
        yield self.label

if __name__ == "__main__":
    pt = get_patient_from_server("2")
    app = PatientAndIdAppTCSS(pt)
    app.run()