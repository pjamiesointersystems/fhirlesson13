from textual.app import App, ComposeResult
from textual.widgets import Header, DataTable, Label
from textual.containers import Container, Horizontal
from fhir.resources.patient import Patient
from getSearchPatients import get_patients_from_server, get_observations_for_patient


class PatientGridApp(App):
    CSS_PATH = "patient_grid.tcss"
    

    def __init__(self, patients: list[Patient]):
        super().__init__()
        self.patients = patients

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            yield Label("Current Patients", id="title")
            yield Label(f"Total: {len(self.patients)}", id="count-label")
        with Container(id="grid-container"):
            self.table = DataTable(zebra_stripes=True)
            yield self.table
        # Main footer with two labels: left and right
        with Horizontal(id="footer-bar"):
           self.footer_label = Label("Select a patient to get the number of observations", id="footer-label")
           self.obs_count_label = Label("", id="obs-count-label")
           yield self.footer_label
           yield self.obs_count_label

    def on_mount(self):
        # Setup table headers
        self.table.add_columns("FHIR ID", "Name", "Sex", "Identifier")
        self.table.cursor_type = "row"
        self.table.show_cursor = True
        for patient in self.patients:
            fhir_id = patient.id or "N/A"
            name = self._get_full_name(patient)
            gender = patient.gender or "N/A"
            identifier = self._get_identifier(patient)
            self.table.add_row(
              f"{fhir_id:<15}",
              f"{name:<40}",
              f"{gender:<10}",
              f"{identifier:<30}",
              key=fhir_id
              )
            print(f"Added {len(self.patients)} rows.")
            print(f"Table has {len(self.table.rows)} rows.")
            self.table.focus() #ensure its interactive and visible
            
    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
         fhir_id = event.row_key.value
         self.footer_label.update(f"Selected FHIR ID: {fhir_id}")
          # Get observations from the FHIR server, using Patient fhir_id
         num_observations = len(get_observations_for_patient(fhir_id))
         self.obs_count_label.update(f"Observations: {num_observations}")

    def _get_full_name(self, patient: Patient) -> str:
        if patient.name:
            name = patient.name[0]
            return " ".join(filter(None, [name.given[0] if name.given else "", name.family]))
        return "N/A"

    def _get_identifier(self, patient: Patient) -> str:
        if patient.identifier and len(patient.identifier) > 0:
            return patient.identifier[0].value or "N/A"
        return "N/A"

# testing
if __name__ == "__main__": 
    patients = get_patients_from_server()
    app = PatientGridApp(patients)
    app.run()