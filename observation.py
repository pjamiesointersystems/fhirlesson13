from datetime import datetime, timedelta
from textwrap import indent
from fhir.resources.observation import Observation
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding
from fhir.resources.quantity import Quantity
from fhir.resources.reference import Reference
from fhir.resources.extension import Extension
from printresource import print_fhir_resource
from zoneinfo import ZoneInfo
import requests
from requests.auth import HTTPBasicAuth

def get_eastern_time_string(minutes_behind: int = 0) -> str:
    # Create a timezone-aware datetime in Eastern Time
    now_eastern = datetime.now(ZoneInfo("America/New_York"))
    # Subtract the specified number of minutes
    adjusted_time = now_eastern - timedelta(minutes=minutes_behind)
    # Convert to ISO 8601 string with offset
    return adjusted_time.isoformat()

def create_heart_rate_observation(subject_id: str, heart_rate_value: int) -> Observation:
    """
    Creates a FHIR Observation resource for heart rate.
    
    :param subject_id: The FHIR Id of the subject (e.g., "Patient/123").
    :param heart_rate_value: The measured heart rate as an integer.
    :return: An Observation resource object.
    """

    observation = Observation(
        status="final",
        category=[
            CodeableConcept(
                coding=[
                    Coding(
                        system="http://terminology.hl7.org/CodeSystem/observation-category",
                        code="vital-signs",
                        display="Vital Signs"
                    )
                ],
                text="Vital Signs"
            )
        ],
        code=CodeableConcept(
            coding=[
                Coding(
                    system="http://loinc.org",
                    code="8867-4",
                    display="Heart rate"
                )
            ],
            text="Heart rate"
        ),
        subject=Reference(reference=f"Patient/{subject_id}"),
        effectiveDateTime = get_eastern_time_string(),
        valueQuantity=Quantity(
            value=heart_rate_value,
            unit="beats/minute",
            system="http://unitsofmeasure.org",
            code="/min"
        )
    )

    return observation

def create_heart_rate_observation2(subject_id: str, heart_rate_value: int) -> Observation:
    """
    Creates a FHIR Observation resource for heart rate.
    
    :param subject_id: The FHIR Id of the subject (e.g., "Patient/123").
    :param heart_rate_value: The measured heart rate as an integer.
    :return: An Observation resource object.
    """
    # Create a Coding object for the heart rate code.
    heart_rate_coding = Coding(
        system="http://loinc.org",
        code="8867-4",
        display="Heart rate"
    )
    
    # Attach the coding to a CodeableConcept object.
    heart_rate_code = CodeableConcept(
        coding=[heart_rate_coding],
        text="Heart rate"
    )
    
    # Create a Coding object for the observation category.
    vital_signs_coding = Coding(
        system="http://terminology.hl7.org/CodeSystem/observation-category",
        code="vital-signs",
        display="Vital Signs"
    )
    
    # Attach the coding to a CodeableConcept for the category.
    vital_signs_category = CodeableConcept(
        coding=[vital_signs_coding],
        text="Vital Signs"
    )
    
    # Construct the Observation resource with the created objects.
    observation = Observation(
        status="final",
        category=[vital_signs_category],
        code=heart_rate_code,
        subject=Reference(reference=f"Patient/{subject_id}"),
        effectiveDateTime = get_eastern_time_string(),
        valueQuantity=Quantity(
            value=heart_rate_value,
            unit="beats/minute",
            system="http://unitsofmeasure.org",
            code="/min"
        )
    )
    
    return observation

def create_heart_rate_observation3(subject_id: str, heart_rate_value: int) -> Observation:
    """
    Creates a FHIR Observation resource for heart rate.
    
    :param subject_id: The FHIR Id of the subject (e.g., "Patient/123").
    :param heart_rate_value: The measured heart rate as an integer.
    :return: An Observation resource object.
    """
    # Create a Coding object for the heart rate code.
    heart_rate_coding = Coding(
        system="http://loinc.org",
        code="8867-4",
        display="Heart rate"
    )
    
    # Attach the coding to a CodeableConcept object.
    heart_rate_code = CodeableConcept(
        coding=[heart_rate_coding],
        text="Heart rate"
    )
    
    # Create a Coding object for the observation category.
    vital_signs_coding = Coding(
        system="http://terminology.hl7.org/CodeSystem/observation-category",
        code="vital-signs",
        display="Vital Signs"
    )
    
    # Attach the coding to a CodeableConcept for the category.
    vital_signs_category = CodeableConcept(
        coding=[vital_signs_coding],
        text="Vital Signs"
    )
    
    
    
    # Construct the Observation resource with the created objects.
    observation = Observation(
        status="final",
        category=[vital_signs_category],
        code=heart_rate_code,
        subject=Reference(reference=f"Patient/{subject_id}"),
        effectiveDateTime = get_eastern_time_string(),
        valueQuantity=Quantity(
            value=heart_rate_value,
            unit="beats/minute",
            system="http://unitsofmeasure.org",
            code="/min"
        )
    )
    
    # Create the custom reporter extension
    reporter_extension = Extension (
    url="http://iscfhir.com/reporter",
    valueString="pjamieso"
    )
    
    # Add the extension to the Observation resource.
    # If the extension list doesn't exist yet, initialize it.
    if not hasattr(observation, "extension") or observation.extension is None:
       observation.extension = []
    
    observation.extension.append(reporter_extension)
    
    return observation

def post_fhir_observation(observation):
    """
    Posts a FHIR Observation resource to a local FHIR server.

    :param observation: A Python Observation instance (from fhir.resources.observation).
    :return: The response object from the POST request.
    """
    # Convert the Observation object to JSON
    observation_json = observation.json()

    # Define the endpoint for posting an Observation
    endpoint = "http://127.0.0.1:8080/csp/healthshare/demo/fhir/r4/Observation"

    # Prepare headers for FHIR JSON
    headers = {
        "Accept": "*/*",
        "content-type": "application/fhir+json",
        "Accept-Encoding": "gzip, deflate, br",
        "Prefer": "return=representation"
    }

    # Send the POST request
    response = requests.post(endpoint, data=observation_json, headers=headers, auth=HTTPBasicAuth('_System', 'ISCDEMO'))

    # Basic status check
    if response.status_code in (200, 201):
        # Parse the returned JSON resource and print its FHIR id.
        resource = response.json()
        fhir_id = resource.get("id")
        print("Observation created with FHIR id:", fhir_id)
    else:
        print(f"Failed to post Observation. Status code: {response.status_code}")
        print("Response:", response.text)

    return response

# class ExtendedObservation(Observation):
#     def __init__(self, **data):
#         # Initialize the base Observation using the provided data.
#         super().__init__(**data)
        
#         # Create the custom reporter extension.
#         reporter_extension = Extension(
#             url="http://iscfhir.com/reporter",
#             valueString="pjamieso"
#         )
        
#         # Add the extension, ensuring any existing extensions are preserved.
#         if self.extension is None:
#             self.extension = [reporter_extension]
#         else:
#             self.extension.append(reporter_extension)



if __name__ == "__main__":
    print("\n--- Creating Observation using sample parameters ---")
    obs = create_heart_rate_observation3("2", 75)
    print_fhir_resource(obs)
    print(obs.json(indent=4))
    response = post_fhir_observation(obs)
    print(response)
    # ext_obs = ExtendedObservation(
    #     status="final",
    #     code={"text": "Heart rate"},
    #     subject={"reference": "Patient/123"}
    # )
    
    # # When printing, the custom extension will be present in the JSON output.
    # print(ext_obs.json(indent=2))

