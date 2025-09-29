import streamlit as st
import textwrap

# --- Helper function for displaying code ---
def _code(cmd: str, language="bash"):
    """Helper for clean code blocks"""
    st.code(textwrap.dedent(cmd).strip(), language=language)

# --- Placeholder Render Functions for conceptual flow ---

def linux_admin_render():
    st.header("2️⃣ Linux Administration: Essential Commands")
    st.markdown("Learn how to navigate the HPC environment.")
    st.info("Content placeholder for essential Linux commands (e.g., `ls`, `cd`, `ssh`, permissions).")

def bash_scripting_render():
    st.header("3️⃣ Bash Scripting: Automating Tasks")
    st.markdown("Automate your job submissions and environment setup.")
    st.info("Content placeholder for Bash scripting concepts (variables, loops, conditionals, functions).")

def containerization_render():
    st.header("4️⃣ Containerization: Docker and Apptainer")
    st.markdown("Ensure reproducibility from your laptop to the cluster.")
    st.info("Content placeholder for container building, pushing, and converting to SIF for HPC.")

def hpc_job_scheduling_render():
    st.header("5️⃣ HPC Job Scheduling (SLURM)")
    st.markdown("How to write and submit efficient SLURM job scripts.")
    st.info("Content placeholder for SLURM directives (`#SBATCH`), partitioning, and resource requests.")

def gpu_performance_render():
    st.header("6️⃣ GPU Performance Basics")
    st.markdown("Tools and concepts for efficient GPU utilization.")
    st.info("Content placeholder for `nvidia-smi`, monitoring, and basic CUDA knowledge.")

def troubleshooting_render():
    st.header("7️⃣ Troubleshooting Techniques")
    st.markdown("Common issues and solutions for AI workloads on HPC.")
    st.info("Content placeholder for debugging job failures, dependency conflicts, and I/O bottlenecks.")

def tools_render():
    st.header("8️⃣ Tools")
    st.markdown("Other useful tools and utilities for AI researchers.")
    st.info("Content placeholder for Git, TensorBoard integration, and data management utilities.")

# --- The NEW Interactive Tool (local_to_hpc_render) ---

def local_to_hpc_render():
    st.header("1️⃣ Interactive Workflow Tool: Local to HPC")
    st.markdown("""
    Use this tool to plan your research workflow, generate boilerplate **Dockerfile** snippets, and automatically draft a corresponding **SLURM execution script** based on your resource needs.
    """)
    st.markdown("---")

    # 1. Local Setup
    with st.container(border=True):
        st.subheader("Step A: Local Environment Setup (Dockerfile)")
        
        col_img, col_form = st.columns([0.4, 0.6])
        
        with col_img:
            # Placeholder for a workflow image
            st.image("https://placehold.co/400x200/4F46E5/FFFFFF?text=Laptop+%E2%86%92+HPC+Workflow", caption="Visualize the container path.")

        with col_form:
            base_image = st.selectbox(
                "1. Select Base Image:",
                ["nvcr.io/nvidia/pytorch:23.09-py3 (Recommended)", "python:3.10-slim", "ubuntu:22.04"],
                key="base_image"
            )
            requirements = st.text_area(
                "2. Required Python Libraries (space/newline separated):",
                value="transformers\ndatasets\naccelerate",
                height=100,
                key="requirements"
            )
            
        st.markdown("**Generated Dockerfile Snippet:**")
        
        # Format requirements for RUN command
        req_list = requirements.split()
        if req_list:
             install_cmd = "pip install --no-cache-dir " + " ".join(req_list)
        else:
             install_cmd = "# No dependencies specified"

        dockerfile_snippet = f"""
        # Base image for CUDA and Python environment
        FROM {base_image.split()[0]}
        
        WORKDIR /app
        COPY . /app/
        
        # Install Python dependencies
        RUN {install_cmd}
        
        # Set the default entry command
        CMD ["python", "train.py"]
        """
        _code(dockerfile_snippet.strip(), language="dockerfile")

    st.markdown("<br>", unsafe_allow_html=True) # Spacer

    # 2. HPC Deployment
    with st.container(border=True):
        st.subheader("Step B: HPC Job Submission (SLURM Script)")
        
        st.markdown("Set your required resources for the compute node.")
        
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            job_name = st.text_input("1. SLURM Job Name:", value="ai_research_job", key="job_name")
            gpu_count = st.slider("3. Required GPUs:", 1, 8, 1, key="gpu_count")
        with col_res2:
            time_limit = st.text_input("2. Time Limit (HH:MM:SS):", value="04:00:00", key="time_limit")
            data_path = st.text_input("4. Host Data Path to Mount:", value="/fs/scratch/user/data/", key="data_path")
        
        if st.button("Generate SLURM Script", type="primary", use_container_width=True):
            st.success("SLURM Script Generated! Remember to replace `my_app.sif` and `/app/train.py` with your actual files.")
            
            slurm_script = f"""
#!/bin/bash
#SBATCH --job-name={job_name}
#SBATCH --account=your_hpc_account
#SBATCH --partition=gpu
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=8
#SBATCH --gres=gpu:{gpu_count}
#SBATCH --time={time_limit}
#SBATCH --output=slurm-%j.out

# --- Execution Command ---
# 1. Assuming 'my_app.sif' has been built from your Docker image.
# 2. --nv: Ensures NVIDIA GPU access
# 3. --bind: Mounts host data path to '/data' inside the container

apptainer exec --nv --bind {data_path}:/data \\
    my_app.sif python /app/train.py \\
    --data_dir /data \\
    --epochs 10

# Use 'sbatch submit.sh' to run this job.
"""
            _code(slurm_script.strip(), language="bash")

# --- Main Application Logic ---

st.set_page_config(page_title="MBZUAI - AI & HPC Workflow", layout="wide")

st.title("MBZUAI Onboarding Guide")
st.subheader("Helping Students & Faculty with Research Workflows in AI")


# Corrected Tabs mapping for logical flow (1️⃣, 2️⃣, 3️⃣...)
tabs = st.tabs([
    "1️⃣ Local to HPC Workflow",       # Index 0: Interactive Tool
    "2️⃣ Linux Administration",        # Index 1
    "3️⃣ Bash Scripting",              # Index 2
    "4️⃣ Containerization",            # Index 3
    "5️⃣ HPC Job Scheduling",          # Index 4
    "6️⃣ GPU Performance Basics",      # Index 5
    "7️⃣ Troubleshooting Techniques",  # Index 6
    "8️⃣ Tools",                       # Index 7
])

# Mapping the corrected tabs to their respective render functions
with tabs[0]:
    local_to_hpc_render() # The new interactive tool
    
with tabs[1]:
    linux_admin_render()
    
with tabs[2]:
    bash_scripting_render()

with tabs[3]:
    containerization_render()

with tabs[4]:
    hpc_job_scheduling_render()

with tabs[5]:
    gpu_performance_render()

with tabs[6]:
    troubleshooting_render()

with tabs[7]:
    tools_render()
