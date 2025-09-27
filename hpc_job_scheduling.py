import streamlit as st

def render():
    st.header("🖥 HPC Job Scheduling with SLURM")
    st.markdown("""
    Submit AI training/analysis jobs to an HPC cluster using SLURM:

    **SLURM Basics:**
    - `sbatch` → submit batch jobs
    - `squeue` → check job queue
    - `scancel` → cancel jobs

    **Job Script Example:**
    """)

    st.subheader("Generate a simple SLURM job script")
    st.code("""#!/bin/bash
#SBATCH --job-name=ai_train
#SBATCH --output=output.log
#SBATCH --error=error.log
#SBATCH --ntasks=1
#SBATCH --gres=gpu:1
#SBATCH --time=02:00:00
#SBATCH --mem=16G

module load cuda/12.1
module load python/3.10

python train_model.py --epochs 50 --batch_size 32
""", language="bash")
