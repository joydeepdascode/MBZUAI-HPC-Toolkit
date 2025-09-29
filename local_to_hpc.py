# local_to_hpc.py
import streamlit as st

# --- Configuration Constants (MBZUAI Context) ---
# Use more generic names to target AI applications in general
# Replaced specific hardcoded values with generic, relevant names
PRIVATE_DOCKER_REGISTRY = "hpc-registry.cscc.local"  # Relevant generic name
HPC_PROJECT_REPOSITORY = "research-containers"       # Relevant generic name
DEFAULT_IMAGE_NAME = "ml-app-base" # Generalized image name
SLURM_ACCOUNT = "ai_research_hpc" # Generalized account name
HPC_DATA_PATH = "/shared/scratch/ai_datasets" # Generalized data path

# --- Generator Functions ---

def generate_dockerfile(base_image_version, app_script_name, app_image_name):
    """
    Generates a generalized Dockerfile content based on user inputs.
    """
    # Using an f-string to embed the constants and user inputs
    return f"""# Dockerfile for MBZUAI AI Application (General)
# Use NVIDIA PyTorch NGC container as base for maximum GPU compatibility
FROM nvcr.io/nvidia/pytorch:{base_image_version} AS builder

# Set the working directory
WORKDIR /app

# Copy and install dependencies
# A 'requirements.txt' file should be placed next to your Dockerfile.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the core AI application code
COPY {app_script_name} .
COPY src /app/src # Copy source code directory if applicable

# Set a default command to run when the container starts
# The command is derived from the main script name
CMD ["python", "{app_script_name}", "--config", "/app/config/default.yaml"]
"""

def generate_slurm_script(optimization_type, nodes, gpus_per_node, time, project_name):
    """
    Generates a customized SLURM job script for various AI tasks.
    Uses the defined constants from the module scope.
    """
    
    # Use the generalized image name for the SIF file
    sif_name = f"{project_name}-v1.0.sif"

    # --- Optimization Specific Logic and Command Setup ---
    if optimization_type == "Highly-Optimized Multi-Node (DDP)":
        # Multi-Node DDP using torchrun (standard for large AI models)
        gpu_request = f"#SBATCH --gpus-per-node={gpus_per_node} \n#SBATCH --constraint=a100|h100"
        nodes_final = nodes
        time_final = time
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
        /app/main_training_script.py --data-path /data/full_corpus
"""
    elif optimization_type == "Single-Node Multi-GPU Training":
        # Single-node, multiple GPU (common for fine-tuning)
        gpu_request = f"#SBATCH --gpus={gpus_per_node}"
        nodes_final = 1
        time_final = time
        run_command = f"""
# --- Single-Node Multi-GPU Fine-Tuning/Inference ---
apptainer exec \\
    --nv \\
    --bind {HPC_DATA_PATH}:/data \\
    $SIF_FILE_PATH \\
    python3 /app/main_training_script.py --mode fine-tune --gpus-per-node {gpus_per_node}
"""
    elif optimization_type == "Low-Memory Fine-Tuning (LoRA/PEFT)":
        # Low-resource configuration, e.g., using a single GPU
        gpu_request = "#SBATCH --gpus=1 \n#SBATCH --mem=64G"
        nodes_final = 1
        time_final = time
        run_command = f"""
# --- Low-Memory PEFT/LoRA Setup ---
apptainer exec \\
    --nv \\
    --bind {HPC_DATA_PATH}:/data \\
    $SIF_FILE_PATH \\
    python3 /app/main_training_script.py --method lora --gpu 0
"""
    elif optimization_type == "Custom/User-Defined Job":
        # A generic template where the user defines everything
        gpu_request = f"#SBATCH --gpus={gpus_per_node} \n#SBATCH --constraint=a100|h100" if gpus_per_node > 0 else "#SBATCH --cpus-per-task=4"
        nodes_final = nodes
        time_final = time
        run_command = f"""
# --- Custom User-Defined Job ---
# Placeholder: Adjust the apptainer exec line and script arguments below
apptainer exec \\
    --nv \\
    --bind {HPC_DATA_PATH}:/data \\
    $SIF_FILE_PATH \\
    /bin/bash -c "echo 'Custom job running...' && python3 /app/my_custom_script.py --nodes $SLURM_JOB_NUM_NODES"
"""
    else: # Default Validation/CPU Test
        gpu_request = "#SBATCH --cpus-per-task=4"
        nodes_final = 1
        time_final = "0-00:10:00"
        run_command = f"""
# --- Default CPU Validation Job ---
apptainer exec \\
    $SIF_FILE_PATH \\
    python3 /app/check_dependencies.py --validate-cpu
"""

    # --- Final SLURM Script Template ---
    return f"""#!/bin/bash
#
# SLURM Job Script: {optimization_type}
# Targeting MBZUAI AI Research Project: {project_name}
#
#SBATCH --job-name={project_name}_{optimization_type.replace(' ', '_').replace('/', '').replace(':', '')}
#SBATCH --account={SLURM_ACCOUNT}
#SBATCH --partition=compute
#SBATCH --nodes={nodes_final}
{gpu_request}
#SBATCH --ntasks-per-node=1
#SBATCH --time={time_final}
#SBATCH --output=slurm-%j.out
#SBATCH --error=slurm-%j.err

echo "--- SLURM JOB START: $(date) ---"

# --- Environment Setup ---
module load apptainer # Load Apptainer runtime module
SIF_FILE_PATH="/global/apps/containers/{sif_name}" 

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
    st.header("Local To HPC: Containerized AI Workflow 📦➡️💻")
    st.markdown("A step-by-step guide to move your PyTorch/AI code from local development to execution on the MBZUAI HPC Cluster using **Docker/Apptainer** and **SLURM**.")
    
    st.info("These tools are designed for MBZUAI’s **Campus Supercomputing Center (CSCC)**, powered by **HPE Apollo 6500 Gen10 Plus** with **AMD EPYC CPUs** and **384 NVIDIA A100 GPUs**.")

    tab1, tab2 = st.tabs(["Container Build Generator 🛠️", "SLURM Jobscript Generator ⚙️"])

    # --------------------------------------------------------------------------
    # Tab 1: Container Build Generator
    # --------------------------------------------------------------------------
    with tab1:
        st.subheader("1. Customize Container Definition (Dockerfile)")
        st.markdown("Generate a general-purpose Dockerfile for any MBZUAI AI application.")
        
        # User Inputs for Customization
        col_t1_1, col_t1_2 = st.columns(2)
        with col_t1_1:
            base_image_version = st.text_input("NVIDIA PyTorch Base Image Tag", 
                                               value="24.08-py3", 
                                               help="Find the latest tags on NGC (e.g., 24.08-py3).",
                                               key="docker_base_tag")
        with col_t1_2:
            app_script_name = st.text_input("Main Application Script File", 
                                            value="train_llm_model.py", 
                                            help="The Python script to run when the container starts.",
                                            key="docker_script_name")
            
        app_image_name = st.text_input("AI Project Name / Image Name", 
                                       value=DEFAULT_IMAGE_NAME, 
                                       help="Used to tag the Docker image and name the SIF file (e.g., my-cv-model).",
                                       key="docker_image_name")

        st.markdown("---")
        st.subheader("Generated Dockerfile")
        
        # Generate and display Dockerfile
        dockerfile_content = generate_dockerfile(base_image_version, app_script_name, app_image_name)
        st.code(dockerfile_content, language='docker')

        st.subheader("2. Docker & Private Registry Commands (Local Machine)")
        # *** CONSTANT REPLACEMENT: Used generic names here ***
        image_tag = f"{PRIVATE_DOCKER_REGISTRY}/{HPC_PROJECT_REPOSITORY}/{app_image_name}:v1.0"
        
        docker_commands = f"""
# 1. Build the Docker image on your local machine
docker build -t {image_tag} .

# 2. Authenticate to the HPC Private Registry
docker login {PRIVATE_DOCKER_REGISTRY} 

# 3. Push the image to the registry for Apptainer access
docker push {image_tag}
"""
        st.code(docker_commands, language='bash')

        st.subheader("3. Apptainer Commands (HPC Login Node)")
        sif_file = f"{app_image_name}_v1.0.sif"
        apptainer_commands = f"""
# 1. Pull the Docker image from the private registry and convert it to a secure SIF file.
apptainer build {sif_file} docker://{image_tag}

# 2. Move the SIF image to a shared global location for job scripts
# mv {sif_file} /global/apps/containers/
"""
        st.code(apptainer_commands, language='bash')
        
    # --------------------------------------------------------------------------
    # Tab 2: SLURM Jobscript Generator
    # --------------------------------------------------------------------------
    with tab2:
        st.subheader("1. Project & Resource Configuration")
        
        project_name = st.text_input("Your Project Name (for Job-Name & SIF)", 
                                     value="my-llm-finetune", 
                                     help="Used in the job name and SIF file path.",
                                     key="slurm_project_name")
        
        # Consolidated Resource Inputs
        col_t2_1, col_t2_2, col_t2_3 = st.columns(3)
        with col_t2_1:
            nodes = st.number_input("Number of Nodes (--nodes)", min_value=1, value=1, step=1, 
                                    help="Total number of compute nodes requested.", key="slurm_nodes_t2")
        with col_t2_2:
            gpus_per_node = st.number_input("GPUs per Node (--gpus/gpus-per-node)", min_value=0, max_value=8, value=4, step=1, 
                                            help="GPUs on each node (0 for CPU-only job).", key="slurm_gpus_t2")
        with col_t2_3:
            time = st.text_input("Max Wall Time (--time)", value="12:00:00", 
                                 help="Time limit format: D-HH:MM:SS or HH:MM:SS (e.g., 1-00:00:00).", key="slurm_time_t2")

        st.markdown("---")
        st.subheader("2. Select Job Profile and Generate")
        
        optimization_options = [
            "Highly-Optimized Multi-Node (DDP)",
            "Single-Node Multi-GPU Training",
            "Low-Memory Fine-Tuning (LoRA/PEFT)",
            "Custom/User-Defined Job",
            "Default CPU Validation Job"
        ]
        
        selected_profile = st.selectbox("Select Optimization Profile", 
                                        optimization_options, 
                                        help="Choose a pre-configured template for your AI task.",
                                        key="slurm_profile_select")
        
        # Use st.session_state to store the script result
        if 'generated_script_t2' not in st.session_state:
            st.session_state.generated_script_t2 = None

        # Single Generate Button
        if st.button(f"Generate SLURM Script for: {selected_profile} 🚀", key="generate_slurm_btn"):
            st.session_state.generated_script_t2 = generate_slurm_script(
                selected_profile, nodes, gpus_per_node, time, project_name
            )

        if st.session_state.generated_script_t2:
            st.markdown("### 3. Generated SLURM Job Script")
            st.code(st.session_state.generated_script_t2, language='bash')
            st.download_button(
                label="Download Job Script",
                data=st.session_state.generated_script_t2,
                file_name=f"{project_name}_job.sh",
                mime="text/plain"
            )
