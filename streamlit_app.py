import streamlit as st
import linux_admin
import bash_scripting
import containerization
import hpc_job_scheduling
import gpu_performance
import troubleshooting
import tools
import local_to_hpc

st.set_page_config(page_title="MBZUAI - AI & HPC Workflow", layout="wide")

st.title("MBZUAI Onboarding Guide")
st.subheader("Helping Students & Faculty with Research Workflows in AI")

# Custom CSS to style the first tab differently
# It targets the first button element inside the st-emotion-cache-r4gssw e1tzin534 (which is the tab container)
# Note: The specific class names (like e1tzin534) might change in future Streamlit versions,
# but using the :nth-child(1) selector on the button within the tab container is a reliable method.
st.markdown("""
<style>
/* Target the first tab button */
.stTabs [data-testid="stTab"] button:nth-child(1) {
    background-color: #008080; /* Teal/Dark Cyan background */
    color: white; /* White text */
    font-weight: bold; /* Bold text */
    border-radius: 5px; /* Rounded corners */
    border: 2px solid #004d4d; /* Darker border */
    padding: 10px 20px; /* More padding */
    box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2); /* Subtle shadow */
    transition: all 0.3s ease-in-out;
}

/* Optional: Style for when the first tab is selected */
.stTabs [data-testid="stTab"] button[aria-selected="true"]:nth-child(1) {
    background-color: #004d4d; /* Even darker background when selected */
    color: #ffcc00; /* Amber/Yellow text when selected */
    border-color: #ffcc00;
}

/* Optional: Hover effect for the first tab */
.stTabs [data-testid="stTab"] button:hover:nth-child(1) {
    background-color: #009999;
}
</style>
""", unsafe_allow_html=True)


# Tabs
tabs = st.tabs([
    "Linux Administration",
    "Bash Scripting",
    "Containerization",
    "HPC Job Scheduling",
    "GPU Performance Basics",
    "Troubleshooting Techniques",
    "Tools",
    "Local To HPC"
])

# The content mapping seems to be swapped compared to the labels,
# but since you asked *not* to change anything else, I'll keep the
# original mapping (which puts 'Local To HPC' content in the 'Linux Administration' tab).
# I've noted this below for clarity.

with tabs[0]:
    # Content for 'Linux Administration' tab - currently rendering local_to_hpc.render()
    local_to_hpc.render()      
with tabs[1]:
    # Content for 'Bash Scripting' tab - currently rendering linux_admin.render()
    linux_admin.render()
with tabs[2]:
    # Content for 'Containerization' tab - currently rendering bash_scripting.render()
    bash_scripting.render()
with tabs[3]:
    # Content for 'HPC Job Scheduling' tab - currently rendering containerization.render()
    containerization.render()
with tabs[4]:
    # Content for 'GPU Performance Basics' tab - currently rendering hpc_job_scheduling.render()
    hpc_job_scheduling.render()
with tabs[5]:
    # Content for 'Troubleshooting Techniques' tab - currently rendering gpu_performance.render()
    gpu_performance.render()
with tabs[6]:
    # Content for 'Tools' tab - currently rendering troubleshooting.render()
    troubleshooting.render()
with tabs[7]:
    # Content for 'Local To HPC' tab - currently rendering tools.render()
    tools.render()
