import streamlit as st
import textwrap

def _code(cmd: str, lang="bash"):
    """Helper for clean code blocks"""
    st.code(textwrap.dedent(cmd).strip(), language=lang)

def render():
    st.header("5️⃣ MBZUAI HPC Environment Overview & Best Practices")
    st.markdown("""
    Goal: Understand the **architecture, resource management, and operational procedures** necessary to effectively run
    large-scale AI and LLM research workloads on the MBZUAI High-Performance Computing (HPC) cluster.
    """)

    st.markdown("---")
    
    # -------------------------
    # 1. Access & Connectivity
    # -------------------------
    st.subheader("1. Access and Initial Setup")
    st.markdown("""
    Access to the cluster is granted via **SSH (Secure Shell)** to the **login node**. 
    **Crucial:** The login node is for management (compiling, submitting jobs, file transfer), **not** for running computations.
    """)
    
    st.markdown("#### Access Command")
    _code("""# Replace 'username' with your assigned cluster username
ssh username@hpc.mbzuai.ac
""", lang="bash")

    st.markdown("#### Port Forwarding for Visual Tools (e.g., TensorBoard)")
    st.markdown("""
    To securely access web-based services (like **TensorBoard** or **Jupyter notebooks**) running on a compute node, you must use **SSH Port Forwarding**.
    """)
    st.info("Example: Forwarding local port 6006 to compute node port 6006.")
    _code("""# Run this from your local machine, then start your service on the compute node.
ssh -L 6006:localhost:6006 username@hpc.mbzuai.ac
""", lang="bash")
    st.markdown("---")

    # -------------------------
    # 2. File System & Data Management
    # -------------------------
    st.subheader("2. File Systems and Data Management (I/O Best Practices)")
    st.markdown("""
    MBZUAI's HPC uses a high-speed parallel file system. Using the correct directory is crucial for job performance and cluster health.
    """)

    st.markdown("#### Key Directories")
    st.markdown(textwrap.dedent("""
    | Directory | Purpose | Performance | Best Practice |
    | :--- | :--- | :--- | :--- |
    | **`/home/$USER`** | Code, configuration files, small scripts, and SLURM logs. | **Slow** | **NEVER** run jobs here. Small files only. |
    | **`/fs/scratch/$USER`** | Primary storage for **large datasets, model checkpoints, and job output**. | **Fast** | **MANDATORY** for training jobs. Data is NOT backed up. |
    | **`/fs/projects/<project_name>`** | Shared space for large, collaborative project data. | **Fast** | Ideal for common datasets used by a team. |
    """))

    st.markdown("#### I/O Optimization for AI (Addressing the Bottleneck)")
    st.warning("""
    **I/O Bottleneck:** Deep learning workloads are often limited by how fast data can be read. Keep your datasets on the fastest available storage (`/fs/scratch`).
    
    **Solution: Container Binding**
    Use Apptainer's `--bind` flag to mount your high-speed scratch data path directly into a simple, accessible path inside your container.
    """)
    
    st.markdown("Example of using Apptainer's bind flag:")
    _code("""# Mounts your scratch data path to /data inside the container
apptainer exec --nv --bind /fs/scratch/$USER/data:/data \\
    your_image.sif python /app/train.py --data_path /data/my_dataset
""", lang="bash")
    
    st.markdown("---")

    # -------------------------
    # 3. Software Environment
    # -------------------------
    st.subheader("3. Software Environment: Modules vs. Containers")
    st.markdown("""
    The cluster uses two complementary systems for managing software dependencies.
    """)
    
    st.info("""
    **Environment Modules (for System Tools):**
    - Manages shared system software (e.g., specific versions of CUDA, Apptainer, Python).
    - Commands: `module avail`, `module load apptainer`, `module list`.
    
    **Containerization (Apptainer/Singularity):**
    - **Preferred for AI:** Ensures full reproducibility of your Python/PyTorch stack across systems. **Do not use Conda environments on compute nodes.**
    - You must often `module load apptainer` in your SLURM script before running your container.
    """)

    st.markdown("---")
    
    # -------------------------
    # NEW SECTION: Infrastructure Deep Dive
    # -------------------------
    st.subheader("4. Cluster Infrastructure and Performance Metrics")
    st.markdown("""
    Understanding the hardware is key to writing efficient job scripts and maximizing research output.
    """)
    
    st.markdown("#### Compute Infrastructure")
    st.markdown("""
    The MBZUAI HPC is built around high-density compute nodes, optimized for large-scale model training:
    * **Core Units:** Each compute node typically houses **8 NVIDIA A100 or H100 GPUs**.
    * **CPU Allocation:** Nodes use high core-count CPUs, often with a ratio of **4-8 CPU cores per GPU** allocated for data loading and pre-processing tasks.
    * **System Memory (RAM):** Nodes feature high RAM capacity (e.g., 512GB to 1TB) to support large batch sizes and in-memory data processing when necessary.
    """)
    
    st.markdown("#### High-Speed Networking (The Backbone of LLM Training)")
    st.markdown("""
    **Distributed training (Multi-GPU/Multi-Node) relies entirely on low-latency, high-bandwidth communication.**
    * **Technology:** The cluster uses **NVIDIA InfiniBand** (e.g., 200Gb/s or faster) as the interconnect between compute nodes.
    * **Importance:** This network speed allows libraries like **PyTorch DDP** or **DeepSpeed** to synchronize model weights (gradients) across hundreds of GPUs with minimal delay. If this network is saturated or incorrectly used, your job performance will plummet.
    """)
    
    st.markdown("#### Performance Metrics (FLOPs)")
    st.markdown("""
    **FLOPs (Floating-Point Operations Per Second)** is the standard measure of GPU performance.
    
    | Metric | Meaning | Relevance to AI |
    | :--- | :--- | :--- |
    | **TFLOPS** | Trillion FLOPs per second | Standard metric for a single GPU. |
    | **PFLOPS** | Quadrillion FLOPs per second | Metric for an entire cluster or large multi-node jobs. |
    
    Researchers should aim for high FLOPs utilization by:
    1.  Using mixed-precision training (`torch.autocast`).
    2.  Ensuring the GPU is always busy (check `nvidia-smi` utilization).
    3.  Using optimized data loaders to prevent CPU/I/O bottlenecks from starving the GPU.
    """)

    st.markdown("---")

    # -------------------------
    # 5. SLURM Job Scheduling
    # -------------------------
    st.subheader("5. SLURM Job Scheduling & Resource Allocation")
    st.markdown("""
    Use SLURM to submit your workload to the cluster's **Compute Nodes**.
    """)
    
    st.markdown("#### Key Partitions (Queues)")
    st.markdown(textwrap.dedent("""
    - **`ai_gpu`**: The primary partition for deep learning training (high-end GPUs, longer time limits).
    - **`low_pri`**: For jobs that can be checkpointed and restarted (cheaper resource access, lower priority).
    - **`debug`**: Short-time limit (e.g., 30 minutes), small resource jobs for quick testing/debugging.
    
    **Action:** Always check resource availability with `sinfo` before submitting long jobs.
    """))

    # --- SLURM Commands (Enhanced) ---
    with st.expander("📋 Essential SLURM Commands"):
        st.markdown("**Everyday SLURM commands you must know:**")

        _code("""# Submit a batch job
sbatch job.sbatch

# Check status of ALL jobs
squeue -u $USER

# Run an interactive command on a compute node (quick debug)
srun --partition=debug --gres=gpu:1 --time=00:15:00 --pty /bin/bash

# Allocate resources for an interactive shell (resource-holding session)
salloc --nodes=1 --ntasks=1 --gres=gpu:1 --time=01:00:00

# View status of partitions and nodes
sinfo

# Cancel a job
scancel <job_id>
""")

        st.markdown("#### Practice")
        st.markdown("""
        1. Request a 30-minute interactive session on the `debug` partition with 1 GPU.
        2. Submit a job using `sbatch` and immediately verify its status with `squeue -u $USER`.
        """)

    # --- SLURM Job Scripts (AI Focus) ---
    with st.expander("📜 Writing Optimized AI Job Scripts"):
        st.markdown("""
        SLURM directives are lines starting with `#SBATCH`. **Be precise to avoid over-requesting and holding up resources.**
        """)

        st.markdown("#### Template: Single-GPU PyTorch/Apptainer Job (`train_gpu.sbatch`)")

        _code("""#!/bin/bash

# --- SLURM Directives ---
# Job Name (Required)
#SBATCH --job-name=MBZUAI_DL_Job
# Account Name (MANDATORY for billing)
#SBATCH --account=your_research_account
# Partition selection
#SBATCH --partition=ai_gpu
# Request 1 node and 1 GPU
#SBATCH --nodes=1
#SBATCH --gres=gpu:1
# Request 8 CPU cores
#SBATCH --cpus-per-task=8
# Request memory (e.g., 64 GB)
#SBATCH --mem=64G
# Set Time Limit (HH:MM:SS)
#SBATCH --time=12:00:00
# Output/Error files
#SBATCH --output=slurm-%j.out
#SBATCH --error=slurm-%j.err

# --- Job Execution ---
module load apptainer

# Execute container, binding data path for I/O efficiency
apptainer exec --nv --bind /fs/scratch/$USER/data:/data \\
    /path/to/your/image.sif python3 /app/train.py --input_dir /data/dataset
""")

        st.markdown("#### Multi-Node Distributed Training (`DDP`)")
        st.warning("""
        **Crucial for Large Models:** Utilize the InfiniBand network correctly by setting up DDP environment variables.
        """)

        _code("""#!/bin/bash
#SBATCH --job-name=LLM_DDP_Job
#SBATCH --partition=ai_gpu
#SBATCH --nodes=2            # Request 2 nodes
#SBATCH --ntasks-per-node=8  # Request 8 tasks (GPUs) per node
#SBATCH --gres=gpu:8         # Request 8 GPUs per node (8*2=16 total GPUs)
#SBATCH --time=72:00:00

# Get node list and set environment variables for PyTorch DDP
NODES=$(scontrol show hostnames $SLURM_JOB_NODELIST)
MASTER_ADDR=$(head -n 1 <<< "$NODES")

export MASTER_PORT=29500
export MASTER_ADDR=$MASTER_ADDR
export WORLD_SIZE=$SLURM_NTASKS
export RANK=$SLURM_PROCID

# Execute the DDP training script using srun
srun apptainer exec --nv your_llm_image.sif \\
    python3 train_ddp.py
""", lang="bash")

    st.markdown("---")

    # -------------------------
    # 6. GPU Monitoring & Debugging
    # -------------------------
    st.subheader("6. GPU Monitoring & Debugging")
    with st.expander("6. GPU Monitoring & Debugging"):
        st.markdown("#### Monitor GPU Usage While Jobs are Running")

        _code("""# Run this on the compute node where your job is executing
nvidia-smi

# Auto-refresh every 2 seconds
watch -n 2 nvidia-smi
""")
        st.warning("""
        **Debugging Tip:** If your job starts but no GPU utilization is shown in `nvidia-smi`, your job is likely running on the CPU! Check these:
        1.  Did you forget the `#SBATCH --gres=gpu:N` directive?
        2.  Did you forget the `--nv` flag in your `apptainer exec` command?
        3.  Is your training framework (PyTorch/TensorFlow) inside the container correctly configured to see CUDA?
        """)
        
    with st.expander("❓ Quick Q&A Drill"):
        st.markdown(textwrap.dedent("""
        1. **What is the high-speed network used for node-to-node communication?**
           - **NVIDIA InfiniBand**, essential for high-performance DDP.
        
        2. **How do you request resources for a job that needs 32 CPU cores and 1TB of memory (CPU-only job)?**
           - Remove `--gres=gpu:N` and use: `#SBATCH --cpus-per-task=32` and `#SBATCH --mem=1024G`.
        
        3. **What is the goal of FLOPs optimization?**
           - To achieve high GPU utilization (e.g., 50%+ of theoretical peak TFLOPS/PFLOPS) to complete training faster.
           
        4. **Where should you **NEVER** run computations?**
           - The login node or your `/home/$USER` directory.
        """))

    st.success("The comprehensive HPC Environment Overview is now complete. You're ready to navigate the MBZUAI cluster effectively! 🚀")
