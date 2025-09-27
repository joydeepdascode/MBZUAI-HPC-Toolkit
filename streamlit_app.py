import streamlit as st
import linux_admin
import bash_scripting
import containerization
import hpc_job_scheduling
import gpu_performance
import troubleshooting

st.set_page_config(page_title="MBZUAI Onboarding Guide", layout="wide")

st.title("MBZUAI Onboarding Guide")
st.subheader("Helping Students & Faculty with Research Workflows in AI")

# Tabs
tabs = st.tabs([
    "Linux Administration",
    "Bash Scripting",
    "Containerization",
    "HPC Job Scheduling",
    "GPU Performance Basics",
    "Troubleshooting Techniques"
])

with tabs[0]:
    linux_admin.render()
with tabs[1]:
    bash_scripting.render()
with tabs[2]:
    containerization.render()
with tabs[3]:
    hpc_job_scheduling.render()
with tabs[4]:
    gpu_performance.render()
with tabs[5]:
    troubleshooting.render()
