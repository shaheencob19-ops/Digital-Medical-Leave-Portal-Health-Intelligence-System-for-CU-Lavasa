# 🏥 CU Lavasa: Medical Leave & Health Intelligence Portal

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red.svg)
![Plotly](https://img.shields.io/badge/Plotly-Interactive-brightgreen.svg)

## 📌 Problem Statement
At the Christ University (Lavasa Campus), the current medical leave process is manually driven by paper. Students are often forced to "chase" multiple faculty members across campus for physical signatures to verify missed periods. This leads to:
* **Academic Loss:** Students miss more lectures while waiting for faculty availability.
* **Administrative Lag:** The Academic Office receives verified data days or weeks after the illness.
* **Blind Management:** The university has no real-time data on whether a flu outbreak or food poisoning incident is occurring in the hostels.

## 🚀 The Solution
This portal digitizes the entire lifecycle of a medical leave application, transforming it from a simple form into a **Strategic Health Intelligence System**.

### 🔄 System Workflow
1. **Student Tier:** Submits a digital application with mandatory medical evidence, specifying periods missed per teacher and subject codes.
2. **Faculty Tier (Parallel Approval):** All concerned teachers receive the request simultaneously. They can verify the specific periods, view the certificate, and Accept/Reject with a reason.
3. **HOD Tier:** After faculty clearance, the HOD performs a departmental audit and final authorization.
4. **Academic Office:** Receives a verified, subject-mapped list ready for "One-Click" updates to Knowledge Pro (KP).
5. **Management Tier:** Accesses a high-level analytics dashboard to monitor campus wellness trends.

## 📊 Strategic Analytics (Data Science in Action)
The "Management Analytics" tab is designed for campus directors to take proactive measures:
* **Predictive Outbreak Timeline:** Detects sudden spikes in sickness applications (e.g., Food Poisoning alerts).
* **Infrastructure Heatmaps:** Identifies if specific departments or blocks have higher illness density (triggering hygiene/ventilation audits).
* **Academic Load Correlation:** Analyzes if stress-related illnesses (Migraines/Mental Health) spike during CIA or exam weeks.

## 🛠️ Technical Stack
* **Frontend/Backend:** [Streamlit](https://streamlit.io/)
* **Data Handling:** [Pandas](https://pandas.pydata.org/)
* **Visualizations:** [Plotly Express](https://plotly.com/python/)
* **Security:** Role-Based Access Control (RBAC) via Admin/Faculty Passcode.

## 📦 Installation & Setup
1. Clone the repository:
   ```bash
   git clone [https://github.com/yourusername/cu-medical-portal.git](https://github.com/yourusername/cu-medical-portal.git)
Install dependencies:

Bash
pip install -r requirements.txt
Run the application:

Bash
streamlit run app.py
🔐 Access Control
Student View: Default (Public)

Admin/Faculty/HOD View: Enter Passcode 1234 in the sidebar to unlock secured roles.

Developed by: Shaheen Haque

MSc Data Science, Christ University, Lavasa Campus
