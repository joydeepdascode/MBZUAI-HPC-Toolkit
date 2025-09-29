# hpc_tool_generator.py
import streamlit as st

# --- Configuration Constants ---
MBZUAI_REGISTRY = "registry.mbzuai.ac/llm-dev"
LLM_IMAGE_NAME = "mha-block-prototype"
SLURM_ACCOUNT = "llm_research_nlp"
HPC_DATA_PATH = "/shared/scratch/llm_datasets/jais_corpus"

def generate_dockerfile(cuda_version="12.1"):
    """Generates the Dockerfile content."""
    return f"""# Dockerfile for MBZUAI LLM Prototype (NLP/IFM Research)
# Base image from NVIDIA's NGC, optimized for PyTorch and GPU
FROM nvcr.io/nvidia/pytorch:2.3.0-py3 AS builder

# Set the working directory for the application
WORKDIR /app

# Copy and install dependencies (assuming 'requirements.txt' is simple, e.g., 'torch==2.3.0')
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the core AI application code (Multi-Head Attention component)
COPY prototype_llm.py .

# Ensure the container runs as a non-root user (HPC security best practice)
# USER 1000 

# Default command for validation
CMD ["python", "prototype_llm.py"]
"""

def generate_slurm_script(optimization_type, nodes, gpus_per_node, time):
    """Generates a customized SLURM job script for LLM training."""
    
    # --- Optimization Specific Logic (MBZUAI Focus) ---
    if optimization_type == "Highly-Optimized for A100/H100":
        # Multi-GPU/Multi-Node setup using torchrun (standard for large LLMs)
        # Assumes the code is DDP-enabled and the Apptainer image contains NCCL/CUDA libs.
        gpu_request = f"#SBATCH --gpus-per-node={gpus_per_node}  # Critical: Request A100/H100 GPUs"
        run_command = f"""
# --- Distributed Training Setup (PyTorch DDP) ---
export MASTER_ADDR=$(scontrol show hostnames $SLURM_JOB_NODELIST | head -n 1)
export MASTER_PORT=29500 # Standard PyTorch port
export NNODES=$SLURM_JOB_NUM_NODES
export NPROC_PER_NODE={gpus_per_node}

apptainer exec \\
    --nv \\
    --bind {HPC_DATA_PATH}:/data \\
    $SIF_FILE_PATH \\
    torchrun \\
        --nnodes $NNODES \\
        --nproc_per_node $NPROC_PER_NODE \\
        --rdzv_id $SLURM_JOB_ID \\
        --rdzv_backend c10d \\
        --rdzv_endpoint $MASTER_ADDR:$MASTER_PORT \\
        /app/prototype_llm.py --input_data /data/tokens.pt --dist-rank $SLURM_PROCID
"""
    elif optimization_type == "Optimized Training Jobscript (Single-Node)":
        # Single-node, multiple GPU (standard for fine-tuning)
        gpu_request = f"#SBATCH --gpus={gpus_per_node}  # Request all {gpus_per_node} GPUs on a single node"
        run_command = f"""
# --- Single-Node Multi-GPU (e.g., fine-tuning Jais) ---
# Assuming the MHA prototype scales across GPUs via DataParallel or DDP on one node
apptainer exec \\
    --nv \\
    --bind {HPC_DATA_PATH}:/data \\
    $SIF_FILE_PATH \\
    python3 /app/prototype_llm.py --input_data /data/tokens.pt --gpus {gpus_per_node}
"""
    elif optimization_type == "Optimization 1: Low-Memory Fine-Tuning (LoRA)":
        # Low-resource configuration, common for smaller experiments or LoRA
        gpu_request = "#SBATCH --gpus-per-node=1  # Only 1 GPU needed for low-memory tasks"
        nodes = 1
        run_command = f"""
# --- Optimization 1: LoRA/QLoRA Fine-Tuning Setup ---
# Designed for efficiency and minimal resource consumption.
apptainer exec \\
    --nv \\
    --bind {HPC_DATA_PATH}:/data \\
    $SIF_FILE_PATH \\
    python3 /app/prototype_llm.py --method LoRA --gpu 0 --data /data/low_res_tokens.pt
"""
    else: # Default CPU Test Jobscript
        gpu_request = "#SBATCH --cpus-per-task=4"
        nodes = 1
        run_command = f"""
# --- Default CPU Test (Validation Job) ---
# Used for quick functional testing of the MHA component before requesting GPUs.
apptainer exec \\
    --bind {HPC_DATA_PATH}:/data \\
    $SIF_FILE_PATH \\
    python3 /app/prototype_llm.py --validate-cpu
"""

    # --- Final SLURM Script Template ---
    return f"""#!/bin/bash
#
# SLURM Job Script: {optimization_type}
# Targeting MBZUAI LLM Research (NLP/IFM)
#
#SBATCH --job-name=MBZUAI_LLM_{optimization_type.replace(' ', '_')}
#SBATCH --account={SLURM_ACCOUNT}             # Research Account
#SBATCH --partition=compute                  # Target the compute partition
#SBATCH --nodes={nodes}
{gpu_request}
#SBATCH --ntasks-per-node=1                  # Typically 1 task per node for PyTorch DDP
#SBATCH --time={time}                        # Time limit (D-HH:MM:SS)
#SBATCH --output=slurm-%j.out
#SBATCH --error=slurm-%j.err

echo "--- SLURM JOB START: $(date) ---"

# --- Environment Setup ---
# Load Apptainer module (required on most MBZUAI HPC systems)
module load apptainer

# Define the path to the Apptainer SIF file
SIF_FILE_PATH="/global/apps/containers/{LLM_IMAGE_NAME}.sif" 

{run_command}

echo "--- SLURM JOB END: $(date) ---"
"""

# --- Streamlit UI ---
st.set_page_config(
    page_title="MBZUAI AI Workflow Generator",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🤖 MBZUAI AI Research Workflow Tool")
st.markdown("Generate reproducible container and SLURM scripts for LLM research (NLP/IFM focus).")

tab1, tab2 = st.tabs(["Container Workflow (Local to HPC)", "SLURM Jobscript Generator"])

with tab1:
    st.header("1️⃣ Image Workflow Generator")
    st.markdown("Generates the necessary steps to move your local MHA prototype to the MBZUAI HPC cluster via the **private registry**.")
    
    st.subheader("Local Development Artifacts")
    
    st.code(generate_dockerfile(), language='docker', label="Dockerfile (The Environment Definition)")
    
    st.subheader("Local Commands (Researcher's Laptop)")
    
    st.markdown("Use your terminal in the project directory:")
    
    docker_commands = f"""
# 1. Build the Docker image, tagging it for the MBZUAI private registry.
docker build -t {MBZUAI_REGISTRY}/{LLM_IMAGE_NAME}:v1.0 .

# 2. Local Validation (Optional, but recommended)
docker run --rm {MBZUAI_REGISTRY}/{LLM_IMAGE_NAME}:v1.0

# 3. Authenticate to the MBZUAI Registry. (Requires prior setup/credentials)
docker login {MBZUAI_REGISTRY.split('/')[0]} 

# 4. Push the image for HPC consumption.
docker push {MBZUAI_REGISTRY}/{LLM_IMAGE_NAME}:v1.0
"""
    st.code(docker_commands, language='bash', label="Docker Build and Push Commands")
    
    st.subheader("HPC Cluster Commands (Login Node)")
    
    apptainer_commands = f"""
# 1. Authenticate Apptainer to the private registry (if required)
# apptainer registry login {MBZUAI_REGISTRY.split('/')[0]}

# 2. Pull the image from the registry and build the secure .sif file.
apptainer build {LLM_IMAGE_NAME}.sif docker://{MBZUAI_REGISTRY}/{LLM_IMAGE_NAME}:v1.0

# 3. Verify the SIF image on the login node.
apptainer exec {LLM_IMAGE_NAME}.sif python3 /app/prototype_llm.py

# 4. Move the SIF to a globally accessible path for SLURM jobs (e.g., /global/apps/containers)
# mv {LLM_IMAGE_NAME}.sif /global/apps/containers/
"""
    st.code(apptainer_commands, language='bash', label="Apptainer Pull and Build Commands")


with tab2:
    st.header("2️⃣ SLURM Job Script Generator")
    st.markdown("Select an optimization profile to generate a production-ready SLURM batch script for your LLM research.")
    
    # SLURM Generator Inputs
    col1, col2, col3 = st.columns(3)
    with col1:
        nodes = st.number_input("Number of Nodes", min_value=1, value=4, step=1, help="Total number of compute nodes to request.")
    with col2:
        gpus_per_node = st.number_input("GPUs per Node", min_value=1, max_value=8, value=8, step=1, help="GPUs on each node (e.g., 8 for A100/H100 nodes).")
    with col3:
        time = st.text_input("Max Wall Time (D-HH:MM:SS)", value="0-08:00:00", help="Time limit for the job.")

    st.markdown("---")
    st.subheader("Optimization Profiles")
    
    # Buttons for generating job scripts
    btn_col1, btn_col2, btn_col3, btn_col4 = st.columns(4)
    
    if btn_col1.button("Highly-Optimized for A100/H100 🚀", help="Multi-Node DDP Training for maximum speed (e.g., Jais pre-training)."):
        script = generate_slurm_script("Highly-Optimized for A100/H100", nodes, gpus_per_node, time)
        st.code(script, language='bash', label="Generated SLURM Script (Multi-Node DDP)")
        
    if btn_col2.button("Optimized Training Jobscript (Single-Node) ⚙️", help="Standard fine-tuning or full-model training on a single, powerful node."):
        script = generate_slurm_script("Optimized Training Jobscript (Single-Node)", 1, gpus_per_node, time)
        st.code(script, language='bash', label="Generated SLURM Script (Single-Node Multi-GPU)")

    if btn_col3.button("Optimization 1: Low-Memory Fine-Tuning (LoRA) 💡", help="For resource-constrained tasks like parameter-efficient fine-tuning (PEFT)."):
        script = generate_slurm_script("Optimization 1: Low-Memory Fine-Tuning (LoRA)", 1, 1, time)
        st.code(script, language='bash', label="Generated SLURM Script (LoRA)")

    if btn_col4.button("Default Validation Job (CPU Only) 🔬", help="Runs on CPU to validate container integrity and environment without consuming GPU time."):
        script = generate_slurm_script("Default CPU Validation Job", 1, 0, time)
        st.code(script, language='bash', label="Generated SLURM Script (CPU Validation)")
