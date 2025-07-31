from turtle import st
from textual.app import App, ComposeResult
from textual.widgets import DataTable, Header, Footer, Button, Static, Label
from textual.containers import Vertical, Horizontal, HorizontalScroll, VerticalScroll
from getSearchPatients import get_patient_from_server
from rich.markup import escape


class PatientWidget(Static):

    def __init__(self, patient, **kwargs):
        super().__init__(**kwargs)
        self.patient = patient
        self.ptName = self.patient.name[0].given[0] + " " + self.patient.name[0].family
        self.ptStrName = escape(str (self.ptName))
        self.ptStrId = escape(str(self.patient.id))
        self.ptStrSSN = escape(str(self.patient.identifier[2].value))
        self.ptStrMS =escape(str(self.patient.maritalStatus.text))

    def compose(self) -> ComposeResult:
        with HorizontalScroll():
            self.patient_name = Label(self.ptStrName)
            self.patient_id = Label(self.ptStrId)
            self.patient_ssn = Label(self.ptStrSSN)
            self.patient_marital_status = Label(self.ptStrMS)
            yield self.patient_name
            yield self.patient_id
            yield self.patient_ssn
            yield self.patient_marital_status




class SimpleApp(App):
    
    CSS_PATH = "patient_label.tcss"
    BINDINGS = [('d', 'toggle_dark', 'Toggle dark mode')]
    
    def __init__(self, patient_id, **kwargs):
        super().__init__(**kwargs)
        self.patient = get_patient_from_server(patient_id)
      

    def compose(self) -> ComposeResult:

        yield Header()
        yield Footer()
        yield PatientWidget(self.patient)
    
        
    def action_toggle_dark(self) -> None:
        return super().action_toggle_dark()
        
        
if __name__ == '__main__':
    app = SimpleApp(4)
    app.run() 