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

# Create two columns, with the second one being much smaller
# col1, col2 = st.columns([0.7, 0.3]) 
# with col1:
#     # Use st.header for the main title
#     st.header("MBZUAI Onboarding Guide") 
# with col2:
#     # You can put a logo or some other small element here if needed
#     st.write("") # Or leave empty if not needed

# # Use st.markdown for the subtitle below the main title
# st.markdown("##### Helping Students & Faculty with Research Workflows in AI")


# Tabs
tabs = st.tabs([
    "Local To HPC - (Tool)",
    "Linux Administration",
    "Bash Scripting",
    "Containerization",
    "HPC Job Scheduling",
    "GPU Performance Basics",
    "Troubleshooting Techniques",
    "Tools"
])

with tabs[0]:
    local_to_hpc.render()      
with tabs[1]:
    linux_admin.render()
with tabs[2]:
    bash_scripting.render()
with tabs[3]:
    containerization.render()
with tabs[4]:
    hpc_job_scheduling.render()
with tabs[5]:
    gpu_performance.render()
with tabs[6]:
    troubleshooting.render()
with tabs[7]:
    tools.render()    
