import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import random

st.set_page_config(page_title="CU Lavasa Medical Intelligence", layout="wide")

# --- UNIVERSITY STRUCTURE ---
CAMPUS_DATA = {
    "1st year MSc Data Science": {"faculties": ["Dr. Lekha Jaybal", "Dr. Lija", "Prof. Milan", "Prof. Ayna", "Prof. Ananya", "Dr. Ashaq", "Prof. Margaret"], "hod": "Dr. Lija"},
    "2nd year MSc Data Science": {"faculties": ["Dr. Lekha Jaybal", "Dr. Lija", "Prof. Milan", "Prof. Ayna", "Prof. Ananya", "Dr. Ashaq", "Prof. Margaret"], "hod": "Dr. Lija"},
    "1st year MBA": {"faculties": ["Prof. Amit", "Dr. Sarah"], "hod": "Dr. Rajesh"},
    "2nd year MBA": {"faculties": ["Dr. Verma", "Prof. Iyer"], "hod": "Dr. Rajesh"},
    "1st year BCA": {"faculties": ["Prof. Naveen", "Dr. Kedar"], "hod": "Dr. Lamba"},
    "BSc Data Science": {"faculties": ["Dr. Arpan Kumar", "Prof. Deepthi"], "hod": "Dr. Lamba"},
    "BSc Ecostats": {"faculties": ["Dr. Sarah", "Prof. Amit"], "hod": "Dr. Rajesh"},
    "MSc GFA": {"faculties": ["Prof. Shanti", "Adv. Mehra"], "hod": "Dr. Kapoor"},
    "BBA": {"faculties": ["Dr. Gupta", "Prof. Iyer"], "hod": "Dr. Kapoor"},
    "BALLB": {"faculties": ["Adv. Mehra", "Dr. Gupta"], "hod": "Prof. Shanti"}
}

if 'db' not in st.session_state:
    st.session_state.db = []

# --- SIDEBAR & ACCESS CONTROL ---
st.sidebar.title("🔐 Portal Access")
access_key = st.sidebar.text_input("Enter Admin/Faculty Key:", type="password")

if access_key == "1234":
    st.sidebar.success("Access Granted")
    available_roles = ["Student Portal", "Faculty Approval", "HOD Approval", "Academic Office", "Management Analytics"]
else:
    available_roles = ["Student Portal"]
    if access_key: st.sidebar.error("Invalid Key")

role = st.sidebar.radio("Navigate Role:", available_roles)

# MOCK DATA GENERATOR
if access_key == "1234" and st.sidebar.button("📊 Populate Strategic Demo Data"):
    reasons = ["Viral Fever", "Food Poisoning", "Migraine", "Injury", "Stress/Mental Health"]
    for _ in range(30):
        d_name = random.choice(list(CAMPUS_DATA.keys()))
        facs = random.sample(CAMPUS_DATA[d_name]["faculties"], 1)
        date_obj = datetime.now() - timedelta(days=random.randint(0, 14))
        st.session_state.db.append({
            "ID": len(st.session_state.db) + 1, "Name": "Mock Student", "RegID": str(random.randint(1000, 9999)),
            "Dept": d_name, "Faculty_Details": {facs[0]: {"periods": random.randint(2, 5), "subject_info": "[MDS101] Core Course"}},
            "Approvals": {facs[0]: "Accepted"}, "HOD": CAMPUS_DATA[d_name]["hod"],
            "Dates": date_obj.strftime("%Y-%m-%d"), "Total_Periods": random.randint(2, 8),
            "Cause": random.choice(reasons), "Status": "Pending HOD" if random.random() > 0.5 else "Completed", 
            "FileData": b"xyz", "FileName": "med.pdf", "FileType": "pdf", "Submitted_At": date_obj.strftime("%Y-%m-%d"),
            "HOD_Rejection_Reason": "", "Faculty_Rejection_Reasons": {}
        })
    st.sidebar.info("30 Strategic Records Generated!")

# --- 1. STUDENT PORTAL ---
if role == "Student Portal":
    st.header("🏥 Student Medical Submission")
    name = st.text_input("Full Name *")
    reg_id = st.text_input("Registration Number *")
    dept = st.selectbox("Your Department *", list(CAMPUS_DATA.keys()))
    selected_faculties = st.multiselect("Select Concerned Faculties *", CAMPUS_DATA[dept]["faculties"])
    
    faculty_data_mapping = {}
    if selected_faculties:
        st.subheader("🔢 Periods and Subjects per Faculty")
        for f in selected_faculties:
            st.markdown(f"**Details for {f}**")
            col1, col2, col3 = st.columns([1, 2, 1])
            with col1: s_code = st.text_input(f"Subject Code ({f})", key=f"sc_{f}")
            with col2: s_name = st.text_input(f"Subject Name ({f})", key=f"sn_{f}")
            with col3: pers = st.number_input(f"Periods missed ({f})", 1, 8, 1, key=f"p_{f}")
            faculty_data_mapping[f] = {"subject_info": f"[{s_code}] {s_name}", "periods": pers}

    st.divider()
    c_a, c_b = st.columns(2)
    with c_a: start_date = st.date_input("Leave From *")
    with c_b: end_date = st.date_input("Leave To *")
    cause = st.text_area("Detailed Reason *")
    file = st.file_uploader("Upload Medical Certificate *", type=['pdf', 'jpg', 'png'])
    
    if st.button("🚀 Submit Application", type="primary"):
        if name and reg_id and selected_faculties and cause and file:
            st.session_state.db.append({
                "ID": len(st.session_state.db) + 1, "Name": name, "RegID": reg_id, "Dept": dept,
                "Faculty_Details": faculty_data_mapping, "Approvals": {f: "Pending" for f in selected_faculties},
                "HOD": CAMPUS_DATA[dept]["hod"], "Dates": f"{start_date} to {end_date}",
                "Total_Periods": sum(d["periods"] for d in faculty_data_mapping.values()), "Cause": cause,
                "Status": "Pending Faculty Approvals", "FileData": file.getvalue(), "FileName": file.name, 
                "FileType": file.type, "Submitted_At": str(start_date), "Faculty_Rejection_Reasons": {}
            })
            st.success("Submitted successfully!")
        else: st.error("Please fill all mandatory fields.")

# --- 2. FACULTY APPROVAL ---
elif role == "Faculty Approval":
    st.header("👨‍🏫 Faculty Approval Dashboard")
    all_f = []
    for d in CAMPUS_DATA.values(): all_f.extend(d["faculties"])
    f_user = st.sidebar.selectbox("Login as Faculty:", sorted(list(set(all_f))))
    pending = [i for i in st.session_state.db if f_user in i['Approvals'] and i['Approvals'][f_user] == "Pending"]
    
    if not pending: st.info(f"No pending requests for {f_user}.")
    for item in pending:
        with st.expander(f"Review: {item['Name']} ({item['RegID']})"):
            st.write(f"**Dates:** {item['Dates']} | **Subject:** {item['Faculty_Details'][f_user]['subject_info']}")
            st.write(f"**Your Periods:** {item['Faculty_Details'][f_user]['periods']} | **Reason:** {item['Cause']}")
            st.download_button("View Certificate", item['FileData'], item['FileName'], key=f"f_{item['ID']}")
            c1, c2 = st.columns(2)
            if c1.button("✅ Accept", key=f"acc_{item['ID']}"):
                item['Approvals'][f_user] = "Accepted"
                if all(v == "Accepted" for v in item['Approvals'].values()): item['Status'] = "Pending HOD"
                st.rerun()
            if c2.button("❌ Reject", key=f"rej_{item['ID']}"):
                st.session_state[f"f_rej_mode_{item['ID']}"] = True
            if st.session_state.get(f"f_rej_mode_{item['ID']}", False):
                reason = st.text_input("Rejection Reason:", key=f"f_msg_{item['ID']}")
                if st.button("Confirm Faculty Rejection", key=f"f_conf_{item['ID']}"):
                    item['Approvals'][f_user] = "Rejected"; item['Status'] = f"Rejected by {f_user}"; st.rerun()

# --- 3. HOD APPROVAL ---
elif role == "HOD Approval":
    st.header("🎓 HOD Final Review")
    pending = [i for i in st.session_state.db if i['Status'] == "Pending HOD"]
    for item in pending:
        with st.expander(f"HOD Review: {item['Name']} ({item['RegID']})"):
            st.write(f"**Dates:** {item['Dates']} | **Total Periods:** {item['Total_Periods']}")
            st.error(f"**Reason for Leave:** {item['Cause']}")
            st.write("**Subject Breakdown:**")
            for f, d in item['Faculty_Details'].items(): st.write(f"- {f}: {d['subject_info']} ({d['periods']} periods) ✅")
            st.download_button("View Certificate", item['FileData'], item['FileName'], key=f"h_{item['ID']}")
            h1, h2 = st.columns(2)
            if h1.button("✅ Final Approve", key=f"ha_{item['ID']}"):
                item['Status'] = "Pending Academic Office"; st.rerun()
            if h2.button("❌ Final Reject", key=f"hr_{item['ID']}"):
                st.session_state[f"hrm_{item['ID']}"] = True
            if st.session_state.get(f"hrm_{item['ID']}", False):
                reason = st.text_input("HOD Rejection Reason:", key=f"hrmsg_{item['ID']}")
                if st.button("Confirm HOD Reject", key=f"hrc_{item['ID']}"):
                    item['Status'] = "Rejected by HOD"; st.rerun()

# --- 4. ACADEMIC OFFICE ---
elif role == "Academic Office":
    st.header("🏢 Academic Office Records")
    pending = [i for i in st.session_state.db if i['Status'] == "Pending Academic Office"]
    if not pending: st.info("No records awaiting KP update.")
    for item in pending:
        with st.container(border=True):
            st.write(f"**Name:** {item['Name']} | **Total Periods:** {item['Total_Periods']} | **HOD:** {item['HOD']} ✅")
            st.subheader("Detailed Mapping for KP Update:")
            for f, d in item['Faculty_Details'].items():
                st.info(f"**Teacher:** {f} | **Subject Info:** {d['subject_info']} | **Periods:** {d['periods']}")
            if st.button("Mark Updated in Knowledge Pro", key=f"ac_{item['ID']}"):
                item['Status'] = "Completed"; st.rerun()

# --- 5. MANAGEMENT ANALYTICS ---
elif role == "Management Analytics":
    st.header("📊 Campus Strategic Health Intelligence")
    
    # STRATEGIC INSTRUCTIONS FOR MANAGEMENT
    with st.expander("📖 INSTRUCTIONS: HOW TO READ AND ACT ON THIS ANALYTICS", expanded=True):
        st.markdown("""
        ### 🔍 How to Read this Dashboard
        1. **KPI Metrics (Top Row):** - **Total Leaves Filed:** Overall volume of health issues.
           - **Total Periods Lost:** The real impact on academic productivity.
           - **Highest Department:** Which group is currently most vulnerable.
        
        2. **Sunburst Hierarchy:** - **Inner Circle:** Shows the Department distribution.
           - **Outer Rings:** Shows the specific sickness causes and their current approval status. Larger sections indicate higher occurrences.
        
        3. **Predictive Outbreak Timeline:** - **Spikes:** Sudden peaks in the graph indicate a potential viral outbreak or high-stress period (e.g., Exam season).
        
        4. **Infrastructure Heatmap:** - **Darker Red Blocks:** Indicate a high concentration of a specific illness within a specific department.
        
        ### 📈 Results and Interpretations
        - **Food Poisoning Spikes:** If the Heatmap shows dark red in 'MBA' or 'Data Science', it indicates an issue with the specific mess hall or cafeteria used by those students.
        - **Stress Peaks:** If the Timeline spikes during CIA weeks with 'Migraines/Stress', the academic load is exceeding student capacity.
        - **Departmental Vulnerability:** If one department is consistently the 'Highest Department', that building's hygiene or ventilation may be compromised.

        ### 🛡️ Recommended Actions
        - **Targeted Audits:** Trigger immediate hygiene inspections for hostels/mess halls associated with 'Food Poisoning' spikes.
        - **Wellness Integration:** Introduce stress-relief sessions or adjust CIA deadlines if Mental Health issues peak.
        - **Resource Allocation:** Ensure the campus clinic is overstocked with medicines relevant to the 'Leading Reason' shown above.
        """)

    if not st.session_state.db: 
        st.warning("Please populate demo data to see strategic insights.")
    else:
        df = pd.DataFrame(st.session_state.db)
        df['Submitted_At'] = pd.to_datetime(df['Submitted_At'])
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Leaves Filed", len(df))
        m2.metric("Total Periods Lost", df['Total_Periods'].sum())
        m3.metric("Highest Department", df['Dept'].mode()[0])
        m4.metric("Leading Reason", df['Cause'].mode()[0])
        
        st.divider()
        col1, col2 = st.columns([1, 1])
        with col1:
            st.subheader("Sunburst Hierarchy (Dept > Cause > Status)")
            fig_sun = px.sunburst(df, path=['Dept', 'Cause', 'Status'], values='Total_Periods', color='Dept')
            st.plotly_chart(fig_sun, use_container_width=True)
        with col2:
            st.subheader("Predictive Outbreak Timeline (Sickness Spikes)")
            trend = df.groupby('Submitted_At').size().reset_index(name='Requests')
            fig_trend = px.area(trend, x='Submitted_At', y='Requests', title="Daily Application Volume Tracking")
            st.plotly_chart(fig_trend, use_container_width=True)
        
        st.subheader("🏢 Infrastructure & Hygiene Intensity Heatmap")
        heat_df = df.groupby(['Dept', 'Cause']).size().reset_index(name='intensity')
        fig_heat = px.density_heatmap(heat_df, x="Dept", y="Cause", z="intensity", color_continuous_scale="Reds", text_auto=True)
        st.plotly_chart(fig_heat, use_container_width=True)