# hpc_job_scheduling.py
import streamlit as st
import textwrap

def _code(cmd: str, lang="bash"):
    """Helper for clean code blocks"""
    st.code(textwrap.dedent(cmd).strip(), language=lang)

def render():
    st.header("4️⃣ HPC & SLURM Basics")
    st.markdown("""
    Goal: Show **familiarity with job scheduling, GPU allocation, and cluster management**  
    using SLURM — the most common HPC workload manager.
    """)

    # -------------------------
    # SLURM Commands
    # -------------------------
    with st.expander("📋 SLURM Commands"):
        st.markdown("**Everyday SLURM commands you must know:**")

        _code("""# Submit a batch job
sbatch job.sbatch

# Run a job interactively
srun --gres=gpu:1 --time=00:30:00 --pty bash

# Allocate resources (interactive session)
salloc --nodes=1 --ntasks=1 --gres=gpu:1 --time=00:30:00

# Cancel a job
scancel <job_id>

# View running jobs
squeue

# View available nodes/partitions
sinfo
""")

        st.subheader("Practice")
        st.markdown("""
        1. Write a simple `job.sbatch` file that sleeps for 60 seconds.  
        2. Submit it with `sbatch job.sbatch`.  
        3. Check status with `squeue`.  
        4. Cancel it with `scancel <job_id>`.  
        """)

    # -------------------------
    # Job Scripts
    # -------------------------
    with st.expander("📜 Job Scripts"):
        st.markdown("**Basic SLURM script template**")

        _code("""#!/bin/bash
#SBATCH --job-name=test_job
#SBATCH --gres=gpu:1
#SBATCH --time=01:00:00
#SBATCH --mem=8G
#SBATCH --output=slurm-%j.out

# Load modules
module load python/3.10

# Run your program
python3 myscript.py
""")

        st.subheader("Practice")
        st.markdown("""
        - Modify script to request **CPU-only job** (remove `--gres=gpu:1`).  
        - Change memory from `8G` → `32G`.  
        - Run a different script `train.py`.  
        """)

    # -------------------------
    # GPU Monitoring
    # -------------------------
    with st.expander("🎮 GPU Monitoring"):
        st.markdown("**Monitor GPU usage while jobs are running**")

        _code("""# Check GPU usage
nvidia-smi

# Auto-refresh every 2 seconds
watch -n 2 nvidia-smi
""")

        st.subheader("Practice")
        st.markdown("""
        1. Submit a GPU job that runs PyTorch and allocates memory.  
        2. Open another terminal and run `watch -n 2 nvidia-smi`.  
        3. Observe memory usage, utilization %, and which process is using GPU.  
        """)

    # -------------------------
    # Exercises
    # -------------------------
    with st.expander("📝 Exercises"):
        st.markdown("""
        1. Write a SLURM script that runs for 10 minutes on **2 GPUs**.  
        2. Run a CPU-only job that requests 16 GB memory.  
        3. Start a job, then cancel it — confirm it disappears from `squeue`.  
        4. Compare GPU utilization while running `sleep` vs `torch.matmul` script.  
        """)

    # -------------------------
    # Drill
    # -------------------------
    with st.expander("❓ Questions — quick Q&A"):
        st.markdown(textwrap.dedent("""
        1. What’s the difference between `sbatch`, `srun`, and `salloc`?  
        - `sbatch`: submit batch job script  
        - `srun`: run job (inside script or interactively)  
        - `salloc`: allocate resources for interactive shell  

        2. How do you request 2 GPUs for 4 hours in SLURM?  
        - `#SBATCH --gres=gpu:2`  
        - `#SBATCH --time=04:00:00`  

        3. How do you monitor GPU usage during a job?  
        - `nvidia-smi` or `watch -n 2 nvidia-smi`  

        4. What does `squeue` vs `sinfo` show?  
        - `squeue`: jobs in queue  
        - `sinfo`: nodes/partitions availability  

        5. How do you kill a stuck job?  
        - `scancel <job_id>`  
        """))

    st.success("HPC Job Scheduling module loaded — you can now submit, monitor, and manage SLURM jobs.")
