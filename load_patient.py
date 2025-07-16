# lesson11_fhir_resources.py
# Lesson 11: Using fhir.resources to Build Simple FHIR Applications

import json
import requests
from fhir.resources.patient import Patient
from fhir.resources.humanname import HumanName
from fhir.resources.contactpoint import ContactPoint


# ---------- Section 1: Unmarshalling (Loading JSON into FHIR resource objects) ----------

def load_patient_from_file():
    with open("example_patient.json") as f:
        data = json.load(f)

    
    patient = Patient(**data)
    print("Patient name:", patient.name[0].given, patient.name[0].family)
    print(f"Patient phone: {patient.telecom[0].use} {patient.telecom[0].value}")
    return patient

# ---------- Run the functions ----------
if __name__ == "__main__":
    print("\n--- Unmarshalling Patient from File ---")
    load_patient_from_file()