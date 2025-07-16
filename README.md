# Lesson 13 – From Data to Design: Crafting FHIR User Interfaces with Textual

Welcome to Lesson 13 of the FHIR Application Development Course!  
This lesson bridges the gap between clinical data and user interface design by guiding learners through building interactive FHIR applications using the **Textual** Python framework.

---

## 🌟 Learning Objectives

By the end of this lesson, you will be able to:

- Understand the unique UI design constraints for healthcare applications (e.g., HIPAA compliance, accessibility, high availability).
- Explain the core architecture and benefits of the `textual` Python framework.
- Build reactive, data-driven interfaces using Textual widgets, containers, events, and actions.
- Use `compose()` and `yield` to construct declarative UI layouts.
- Implement FHIR data visualization using terminal-based interfaces.

---

## 🏥 Why User Interface Matters in Healthcare

Healthcare applications face specialized UI challenges, including:

- 📜 Data Privacy & Regulatory Compliance (HIPAA, HL7, FHIR)
- 🧑‍⚕️ Diverse Clinical User Requirements
- ⚡ Low Latency & High Reliability
- 🔒 Security and Full Audit Trails
- 🌐 Accessibility and Inclusive Design
- 📈 High Data Integrity and Scalability

---

## 🧰 Framework Overview: [Textual](https://github.com/Textualize/textual)

`Textual` is a Python-native framework for building interactive TUI (Textual User Interfaces) using modern declarative programming techniques.

### 🔧 Key Features

- **Pythonic API** – No JavaScript or web tech needed
- **Composable Widgets** – `Label`, `Static`, `DataTable`, etc.
- **Declarative Layouts** – Built using `compose()` + `yield`
- **Event System** – React to user actions or internal state changes
- **Action Bindings** – Use `BINDINGS` and `action_` methods for command execution
- **TCSS Styling** – Terminal-native styling with .tcss files

---

## 🧱 Lesson Demo App: `FhirUIApp`

The sample app demonstrates a tabbed FHIR interface with two views:

```text
FhirUIApp (App)
└── TabbedContent
    ├── TabPane ("Patients")
    │   └── Vertical
    │       ├── Label ("Patients")
    │       └── DataTable (self.patient_table)
    └── TabPane ("Observations")
        └── Vertical
            ├── Label ("Observations")
            └── DataTable (self.obs_table)
ode Highlights
compose() – Builds the UI tree using yield

post_message() – Sends messages up the widget tree

@on_<event> – Handles incoming messages

action_<name>() – Defines user-invokable app behaviors

Sample Action Binding
python
Copy
Edit
class MyApp(App):
    BINDINGS = [("r", "reload", "Reload data")]

    async def action_reload(self):
        await self.fetch_new_data()
        self.log("Data reloaded!")
🎨 Styling with TCSS
Textual uses .tcss for styling components:

tcss
Copy
Edit
Label {
    padding: 1 2;
    border: round green;
    background: $surface;
}
Padding adds space inside the widget

Margin adds space outside the widget

🚀 Getting Started
Clone the repo:


git clone https://github.com/pjamiesointersystems/fhirlesson13.git
cd fhirlesson13
Create a virtual environment:


python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
Install requirements:


pip install -r requirements.txt
Run the app:


python app.py
🛠 Backend Integration (Optional)
Future lessons revisit integration with the Django REST Framework (DRF) to build secure, browsable APIs for FHIR data.

👥 Authors
Patrick W. Jamieson, M.D. – Technical Product Manager

Russ Leftwich, M.D. – Senior Clinical Advisor, Interoperability

📄 License
This repository is released under the MIT License.

🙏 Acknowledgments
Thanks to the Textualize team for their outstanding work in building Python-native UI tooling.


