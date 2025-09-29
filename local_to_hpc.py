# local_to_hpc.py
import streamlit as st

# --- Configuration Constants (MBZUAI Context) ---
# NOTE: Replace with actual private registry details
MBZUAI_REGISTRY_HOST = "registry.mbzuai.ac" 
MBZUAI_PROJECT_REPO = "llm-dev"
LLM_IMAGE_NAME = "mha-prototype"
SLURM_ACCOUNT = "llm_research_nlp"
HPC_DATA_PATH = "/shared/scratch/llm_datasets" # Common shared filesystem path

# --- Generator Functions ---

def generate_dockerfile():
    """Generates the Dockerfile content."""
    return f"""# Dockerfile for MBZUAI LLM Prototype (NLP/IFM Research)
# Use NVIDIA PyTorch NGC container as base for maximum GPU compatibility
FROM nvcr.io/nvidia/pytorch:2.3.0-py3 AS builder

# Set the working directory
WORKDIR /app

# Copy and install dependencies
# A 'requirements.txt' file should be placed next to your Dockerfile.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the core AI application code (e.g., your training script)
COPY train_llm_model.py .
COPY src /app/src # Copy source code directory if applicable

# Set a default command to run when the container starts
CMD ["python", "train_llm_model.py", "--config", "/app/config/default.yaml"]
"""

def generate_slurm_script(optimization_type, nodes, gpus_per_node, time):
    """Generates a customized SLURM job script for LLM training."""
    
    # --- Optimization Specific Logic and Command Setup ---
    if optimization_type == "Highly-Optimized for A100/H100":
        # Multi-Node DDP using torchrun (standard for large LLMs)
        gpu_request = f"#SBATCH --gpus-per-node={gpus_per_node} \n#SBATCH --constraint=a100|h100"
        run_command = f"""
# --- Distributed Training Setup (PyTorch DDP/Apptainer) ---
export MASTER_ADDR=$(scontrol show hostnames $SLURM_JOB_NODELIST | head -n 1)
export MASTER_PORT=29500 
export NNODES=$SLURM_JOB_NUM_NODES
export NPROC_PER_NODE={gpus_per_node}

# The Apptainer container provides the environment and libs (CUDA/NCCL)
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
        /app/train_llm_model.py --data-path /data/full_corpus
"""
    elif optimization_type == "Optimized Training Jobscript":
        # Single-node, multiple GPU (common for fine-tuning)
        gpu_request = f"#SBATCH --gpus={gpus_per_node}"
        nodes = 1
        run_command = f"""
# --- Single-Node Multi-GPU Fine-Tuning ---
# Using all GPUs on a single node for fast, single-process training
apptainer exec \\
    --nv \\
    --bind {HPC_DATA_PATH}:/data \\
    $SIF_FILE_PATH \\
    python3 /app/train_llm_model.py --data-path /data/finetune_subset --gpus-per-node {gpus_per_node}
"""
    elif optimization_type == "Optimization 1: Low-Memory Fine-Tuning (LoRA)":
        # Low-resource configuration, e.g., using a single GPU
        gpu_request = "#SBATCH --gpus=1 \n#SBATCH --mem=64G"
        nodes = 1
        run_command = f"""
# --- Optimization 1: PEFT/LoRA Fine-Tuning Setup ---
# Designed for efficiency on a single GPU (e.g., QLoRA for a 7B model)
apptainer exec \\
    --nv \\
    --bind {HPC_DATA_PATH}:/data \\
    $SIF_FILE_PATH \\
    python3 /app/train_llm_model.py --method lora --gpu 0 --data /data/peft_data
"""
    else: # Default Validation/CPU Test
        gpu_request = "#SBATCH --cpus-per-task=4"
        nodes = 1
        run_command = f"""
# --- Default CPU Validation Job ---
# Quick check of environment and dependencies before resource-intensive GPU use.
apptainer exec \\
    $SIF_FILE_PATH \\
    python3 /app/train_llm_model.py --validate-cpu
"""

    # --- Final SLURM Script Template ---
    return f"""#!/bin/bash
#
# SLURM Job Script: {optimization_type}
# Targeting MBZUAI LLM Research
#
#SBATCH --job-name=MBZUAI_LLM_{optimization_type.replace(' ', '_').replace(':', '')}
#SBATCH --account={SLURM_ACCOUNT}
#SBATCH --partition=compute
#SBATCH --nodes={nodes}
{gpu_request}
#SBATCH --ntasks-per-node=1
#SBATCH --time={time}
#SBATCH --output=slurm-%j.out
#SBATCH --error=slurm-%j.err

echo "--- SLURM JOB START: $(date) ---"

# --- Environment Setup ---
module load apptainer # Load Apptainer runtime module
SIF_FILE_PATH="/global/apps/containers/{LLM_IMAGE_NAME}_v1.0.sif" 

# Check if SIF exists (best practice)
if [ ! -f "$SIF_FILE_PATH" ]; then
    echo "ERROR: Apptainer SIF file not found at $SIF_FILE_PATH"
    exit 1
fi

{run_command}

echo "--- SLURM JOB END: $(date) ---"
"""

# --- Streamlit Renderer Function (called by main_app.py) ---

def render():
    """Renders the Streamlit UI for the Local To HPC tab."""
    st.header("Local To HPC: Containerized Research Workflow 📦➡️💻")
    st.markdown("A step-by-step guide to move your PyTorch/LLM code from local development to execution on the MBZUAI HPC Cluster using **Docker/Apptainer** and **SLURM**.")

    tab1, tab2 = st.tabs(["Container Build Workflow", "SLURM Jobscript Generator"])

    # --------------------------------------------------------------------------
    # Tab 1: Container Build Workflow
    # --------------------------------------------------------------------------
    with tab1:
        st.subheader("1. Dockerfile (Local Environment Definition)")
        st.info("Define your environment in a **`Dockerfile`**. It starts from a trusted, GPU-ready base image (e.g., NVIDIA's NGC PyTorch image).")
        st.code(generate_dockerfile(), language='docker', label="Dockerfile")

        st.subheader("2. Docker & Private Registry Commands (Local Machine)")
        image_tag = f"{MBZUAI_REGISTRY_HOST}/{MBZUAI_PROJECT_REPO}/{LLM_IMAGE_NAME}:v1.0"
        
        docker_commands = f"""
# 1. Build the Docker image on your local machine
docker build -t {image_tag} .

# 2. Authenticate to the MBZUAI Private Registry
docker login {MBZUAI_REGISTRY_HOST} 

# 3. Push the image to the registry for Apptainer access
docker push {image_tag}
"""
        st.code(docker_commands, language='bash', label="Docker Build and Push Commands")

        st.subheader("3. Apptainer Commands (HPC Login Node)")
        st.warning("Ensure the **Apptainer module is loaded** (`module load apptainer`) before running these commands on the HPC login node.")
        
        apptainer_commands = f"""
# 1. Pull the Docker image from the private registry and convert it to a secure SIF file.
# The SIF file is the native container format for HPC (Apptainer/Singularity).
apptainer build {LLM_IMAGE_NAME}_v1.0.sif docker://{image_tag}

# 2. Verify the SIF image (Optional)
apptainer exec --nv {LLM_IMAGE_NAME}_v1.0.sif python3 /app/train_llm_model.py --version

# 3. Move the SIF image to a shared global location for job scripts
# mv {LLM_IMAGE_NAME}_v1.0.sif /global/apps/containers/
"""
        st.code(apptainer_commands, language='bash', label="Apptainer Pull and SIF Creation Commands")
        
    # --------------------------------------------------------------------------
    # Tab 2: SLURM Jobscript Generator
    # --------------------------------------------------------------------------
    with tab2:
        st.subheader("SLURM Resource Configuration")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            nodes = st.number_input("Number of Nodes (--nodes)", min_value=1, value=4, step=1, help="Total number of compute nodes (for distributed training).")
        with col2:
            gpus_per_node = st.number_input("GPUs per Node (--gpus-per-node)", min_value=1, max_value=8, value=8, step=1, help="GPUs on each node (e.g., 8 for A100/H100 nodes).")
        with col3:
            time = st.text_input("Max Wall Time (--time)", value="1-00:00:00", help="Time limit format: D-HH:MM:SS (e.g., 1 day, 0 hours, 0 minutes).")

        st.markdown("---")
        st.subheader("AI Optimization Profiles (LLM Focused)")
        
        btn_col1, btn_col2, btn_col3, btn_col4 = st.columns(4)
        
        script = None
        
        with btn_col1:
            if st.button("Highly-Optimized for A100/H100 🚀", help="Multi-Node Distributed Data Parallel (DDP) Pre-training."):
                script = generate_slurm_script("Highly-Optimized for A100/H100", nodes, gpus_per_node, time)
                
        with btn_col2:
            if st.button("Optimized Training Jobscript (Single-Node) ⚙️", help="Fine-tuning or training on a single, powerful GPU node."):
                script = generate_slurm_script("Optimized Training Jobscript", 1, gpus_per_node, time)

        with btn_col3:
            if st.button("Optimization 1: Low-Memory Fine-Tuning (LoRA) 💡", help="Parameter-Efficient Fine-Tuning (PEFT) using minimal GPU resources."):
                script = generate_slurm_script("Optimization 1: Low-Memory Fine-Tuning (LoRA)", 1, 1, time)

        with btn_col4:
            if st.button("Default Validation Job (CPU Only) 🔬", help="Runs quick checks of the container integrity and dependencies."):
                script = generate_slurm_script("Default CPU Validation Job", 1, 0, "0-00:10:00") # Short time limit

        if script:
            st.markdown("### Generated SLURM Job Script")
            st.code(script, language='bash')
            st.download_button(
                label="Download Job Script",
                data=script,
                file_name="mbzuai_llm_job.sh",
                mime="text/plain"
            )

# Example of what the main file (e.g., main_app.py) would look like:
# if __name__ == '__main__':
#     # This block would only be for testing the module directly
#     render()
