import json
import requests
from fhir.resources.patient import Patient
from fhir.resources.humanname import HumanName
from fhir.resources.contactpoint import ContactPoint
from fhir.resources.address import Address



def patient_from_file(file_path):
    patient = Patient.parse_file(file_path)
    return patient

def print_fhir_resource(resource):
    """
    Recursively prints all non-None fields (including nested fields)
    from a FHIR resource object.
    """
    def print_non_none(data, prefix=""):
        # If data is a dictionary, recurse into each key/value.
        if isinstance(data, dict):
            for key, value in data.items():
                if value is not None:
                    print_non_none(value, prefix=f"{prefix}{key}.")
        # If data is a list, recurse into each item.
        elif isinstance(data, list):
            for idx, item in enumerate(data):
                if item is not None:
                    print_non_none(item, prefix=f"{prefix}[{idx}].")
        else:
            # data is a scalar (string, int, bool, etc.)
            # prefix[:-1] removes the trailing '.' or bracket from the last concatenation
            print(f"{prefix[:-1]}: {data}")

    # Convert the resource object into a dict
    resource_dict = resource.dict()
    # Start recursive printing
    print_non_none(resource_dict)


# ---------- Run the functions ----------
if __name__ == "__main__":
    print("\n--- Unmarshalling Patient from File ---")
    pt = patient_from_file("peter_patient.json")
    ad = pt.address[0]
    con = pt.contact[0]
    #print(pt)
    print_fhir_resource(pt)
