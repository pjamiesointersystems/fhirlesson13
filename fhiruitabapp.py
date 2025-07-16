from textual.app import App, ComposeResult
from textual.widgets import Tabs, TabPane, Tab, DataTable, Label, Header, Footer, Static, TabbedContent
from textual.containers import Container, Horizontal, Vertical
from fhir.resources.patient import Patient
from fhir.resources.observation import Observation
from textual.message import Message
from textual.events import Event
from textual.scroll_view import ScrollView
from fhir.resources.patient import Patient
from fhir.resources.observation import Observation
from rich.style import Style
from getSearchPatients import get_patients_from_server, get_observations_for_patient

class FhirUIApp(App):
    CSS_PATH = "fhir_ui.tcss"
    BINDINGS = [
        ("ctrl+q", "quit", "Quit the app")
    ]

    def action_quit(self) -> None:
        """Action to quit the app."""
        self.exit()

    def __init__(self, patients: list[Patient], observations: dict[str, list[Observation]]):
        super().__init__()
        self.patients = patients
        self.observations = observations  # Dict[patient_id] = list of Observations
        self.selected_patient_id = None

    def compose(self) -> ComposeResult:
        with TabbedContent():
            # Create and yield the Tabs widget, and store a reference for later use.
            with TabPane("Patients", id='patients-tab'):
                yield self._build_patient_view()
            with TabPane("Observations", id='observations-tab'):
                yield self._build_observation_view()
            
    def on_mount(self):
        pass

    def _build_patient_view(self):
        self.patient_table = DataTable(zebra_stripes=True)
        self.patient_table.add_columns("FHIR ID", "Name", "Sex", "Identifier")
        #enable row selection
        self.patient_table.show_cursor = True
        self.patient_table.cursor_type = "row"

        for patient in self.patients:
            fhir_id = patient.id or "N/A"
            name = self._get_name(patient)
            gender = patient.gender or "N/A"
            identifier = self._get_identifier(patient)
            self.patient_table.add_row(fhir_id, name, gender, identifier, key=fhir_id)

        return Vertical(Label("Patients"), self.patient_table)

    def _build_observation_view(self):
        self.obs_table = DataTable(zebra_stripes=True)
        self.obs_table.add_columns("Category", "Code", "Effective", "Value")
        
        return Vertical(Label("Observations"), self.obs_table)

    def on_data_table_row_selected(self, event: DataTable.RowSelected):
        print("Row selected:", event.row_key.value)
        self.selected_patient_id = event.row_key.value
        self.query_one(Tabs).active = "observations-tab"  # Switch to observation tab
        self._load_observations_for_patient(self.selected_patient_id)

    def _load_observations_for_patient(self, patient_id: str):
       self.obs_table.clear()
       obs_list = get_observations_for_patient(patient_id)

       for obs in obs_list:
          category = self._get_text(obs.category)
          code = obs.code.text or "N/A"
          effective = getattr(obs, "effectiveDateTime", None) or getattr(obs, "effectivePeriod", "N/A")
        
          # New logic for value:
          if hasattr(obs, "valueString") and obs.valueString is not None:
             value = obs.valueString
          elif hasattr(obs, "valueCodeableConcept") and obs.valueCodeableConcept is not None:
             # Expecting valueCodeableConcept to have a coding list, get the first display value.
             codeable = obs.valueCodeableConcept
             if hasattr(codeable, "coding") and codeable.coding and len(codeable.coding) > 0:
                value = codeable.coding[0].display or "N/A"
             else:
                value = "N/A"
          elif hasattr(obs, "valueQuantity") and obs.valueQuantity is not None:
             quantity = obs.valueQuantity
             num_value = str(quantity.value)
             unit = quantity.unit if hasattr(quantity, "unit") and quantity.unit else ""
             value = f"{num_value} {unit}".strip()
          else:
            value = "N/A"
        
          self.obs_table.add_row(category, code, str(effective), value)


    def _get_text(self, coding_list):
        if coding_list and isinstance(coding_list, list) and coding_list[0].coding:
            return coding_list[0].coding[0].display or coding_list[0].coding[0].code
        return "N/A"

    def _get_name(self, patient):
        if patient.name:
            n = patient.name[0]
            return f"{n.given[0]} {n.family}" if n.given else n.family
        return "N/A"

    def _get_identifier(self, patient):
        return patient.identifier[0].value if patient.identifier else "N/A"
    
    
if __name__ == "__main__":
   patients = get_patients_from_server()
   app = FhirUIApp(patients, None)
   app.run() 