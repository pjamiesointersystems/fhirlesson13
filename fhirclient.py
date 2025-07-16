# lesson11_fhir_resources.py
# Lesson 11: Using fhir.resources to Build Simple FHIR Applications

import json
import requests
from fhir.resources.patient import Patient
from fhir.resources.humanname import HumanName
from fhir.resources.contactpoint import ContactPoint
from fhir.resources.observation import Observation
from fhir.resources.condition import Condition

# ---------- Section 1: Unmarshalling (Loading JSON into FHIR resource objects) ----------

def load_patient_from_file():
    with open("example_patient.json") as f:
        data = json.load(f)
    patient = Patient(**data)
    print("Patient name:", patient.name[0].given, patient.name[0].family)
    return patient


# ---------- Section 2: Marshalling (Creating FHIR resource objects in Python) ----------

def create_patient():
    name = HumanName(given=["Alice"], family="Smith")
    telecom = ContactPoint(system="phone", value="555-1234", use="mobile")
    patient = Patient(name=[name], gender="female", birthDate="1990-05-01", telecom=[telecom])
    print("Created Patient JSON:")
    print(patient.json(indent=2))
    return patient


# ---------- Section 3: Working with FHIR Server Data ----------

def fetch_patient_from_server():
    fhir_url = "https://hapi.fhir.org/baseR4/Patient/example"
    response = requests.get(fhir_url)
    if response.status_code == 200:
        patient = Patient(**response.json())
        print("Patient from FHIR server:", patient.name[0].given, patient.name[0].family)
        return patient
    else:
        print("Failed to fetch Patient. Status code:", response.status_code)
        return None


# ---------- Section 4: Bonus - Observation and Condition Examples ----------

def load_observation_from_file():
    with open("example_observation.json") as f:
        data = json.load(f)
    observation = Observation(**data)
    print("Observation Code:", observation.code.text)
    return observation

def load_condition_from_file():
    with open("example_condition.json") as f:
        data = json.load(f)
    condition = Condition(**data)
    print("Condition Description:", condition.code.text)
    return condition


# ---------- Run the functions ----------
if __name__ == "__main__":
    print("\n--- Unmarshalling Patient from File ---")
    load_patient_from_file()

    print("\n--- Creating Patient from Scratch ---")
    create_patient()

    print("\n--- Fetching Patient from FHIR Server ---")
    fetch_patient_from_server()

    print("\n--- Loading Observation from File ---")
    load_observation_from_file()

    print("\n--- Loading Condition from File ---")
    load_condition_from_file()
