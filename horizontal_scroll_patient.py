from textual.app import App
from textual.widgets import Static, Label
from textual.containers import HorizontalScroll
from rich.markup import escape
from rich.text import Text
from fhir.resources.patient import Patient
from getSearchPatients import get_patient_from_server

NUM_BOXES = 20

class PatientHorizontalScrollApp(App):
    
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

        with HorizontalScroll():
           # Create a Label widget similarly for the patient id.
          self.label = Label()
          self.label.add_class("patientId")
          patient_id_str = escape(str(self.patient.id))
          patient_id_text = Text(f"Patient ID: {patient_id_str}")
          self.label.update(patient_id_text)
          yield self.label 
          
          self.extralabel = Label()
          self.extralabel.add_class("patientDetails")
          patient_ssn = escape(str(self.patient.identifier[2].value))
          patient_ssn_text = Text(f"Social Security No.: {patient_ssn}")
          self.extralabel.update(patient_ssn_text)
          yield self.extralabel
          
          self.extralabel1 = Label()
          self.extralabel1.add_class("patientDetails")
          patient_marital_status = escape(str(self.patient.maritalStatus.text))
          patient_marital_text = Text(f"Marital Status: {patient_marital_status}")
          self.extralabel1.update(patient_marital_text)
          yield self.extralabel1
          
          self.extralabel2 = Label()
          self.extralabel2.add_class("patientDetails")
          patient_telecom = escape(str(self.patient.telecom[0].system + ":" + self.patient.telecom[0].value))
          patient_telecom_text = Text(f"Telecom: {patient_telecom}")
          self.extralabel2.update(patient_telecom_text)
          yield self.extralabel2
          
          self.extralabel3 = Label()
          self.extralabel3.add_class("patientDetails")
          patient_address = escape(str(self.patient.address[0].line[0] + ", " + self.patient.address[0].city + ", " + self.patient.address[0].state))
          patient_address_text = Text(f"Address: {patient_address}")
          self.extralabel3.update(patient_address_text)
          yield self.extralabel3
    

if __name__ == "__main__":
    pt = get_patient_from_server("2")
    app = PatientHorizontalScrollApp(pt)
    app.run()