# containerization.py
import streamlit as st
import textwrap

def _code(cmd: str):
    """Helper for clean bash code blocks"""
    st.code(textwrap.dedent(cmd).strip(), language="bash")

def render():
    st.header("3️⃣ Containerization Mastery")
    st.markdown("""
    Goal: Understand **why and how containers are used in HPC labs**,  
    and learn to **run AI workloads inside them** with Docker and Singularity (Apptainer).
    """)

    # -------------------------
    # Docker Basics
    # -------------------------
    with st.expander("🐳 Docker Basics"):
        st.markdown("**Key Docker commands for AI/ML workloads**")
        _code("""# Run a container interactively
docker run -it ubuntu:20.04 bash

# List running containers
docker ps

# Execute a command inside a container
docker exec -it <container_id> /bin/bash

# Build an image from Dockerfile
docker build -t my-ml-image .
""")

        st.subheader("Practice: Build a container with Python + ML libs")
        _code("""# Example Dockerfile
FROM python:3.10-slim

RUN apt-get update && apt-get install -y git \
    && pip install torch torchvision transformers

CMD ["python3"]
""")

        st.markdown("""
        - Save this as `Dockerfile`  
        - Build it: `docker build -t ai-container .`  
        - Run it: `docker run -it ai-container`  
        """)

    # -------------------------
    # Singularity / Apptainer
    # -------------------------
    with st.expander("📦 Singularity (Apptainer)"):
        st.markdown("""
        HPC environments often prefer **Singularity (Apptainer)** because:  
        - Rootless execution (safer on shared clusters)  
        - Multi-user & HPC-friendly  
        - Easy conversion from Docker images  
        """)

        st.subheader("Convert Docker → Singularity")
        _code("""# Convert a Docker image into Singularity image
singularity build image.sif docker://pytorch/pytorch:2.0.0-cuda11.7-cudnn8-runtime
""")

        st.subheader("Run containerized workloads")
        _code("""# Run a Python command inside Singularity
singularity exec image.sif python3 -c "import torch; print(torch.__version__)"
""")

        st.subheader("Practice: Build & test Torch container")
        _code("""# Example
singularity exec image.sif python3 - << 'EOF'
import torch
print("Torch version:", torch.__version__)
print("CUDA available:", torch.cuda.is_available())
EOF
""")

    # -------------------------
    # HPC Integration
    # -------------------------
    with st.expander("⚡ HPC Integration with SLURM"):
        st.markdown("""
        Containers are often used **inside SLURM jobs** to isolate dependencies.  
        Typical workflow: write a SLURM script that launches a Singularity container.
        """)

        st.subheader("SLURM + Singularity Example")
        _code("""#!/bin/bash
#SBATCH --job-name=singularity_test
#SBATCH --gres=gpu:1
#SBATCH --time=01:00:00
#SBATCH --output=slurm-%j.out

# Load Singularity module
module load singularity

# Run Python script inside container
singularity exec image.sif python3 train_model.py
""")

        st.subheader("Practice: Run containerized Python script inside SLURM")
        st.markdown("""
        1. Write a Python script `train_model.py` that prints GPU info.  
        2. Package dependencies inside Docker → convert to Singularity.  
        3. Submit the SLURM job using `sbatch job.sbatch`.  
        """)

    # -------------------------
    # Exercises
    # -------------------------
    with st.expander("📝 Exercises"):
        st.markdown("""
        1. Build a Dockerfile that installs TensorFlow and NLTK.  
        2. Convert your Docker image into Singularity `.sif` format.  
        3. Write a SLURM script to run a containerized PyTorch job.  
        4. Test container isolation by running `hostname` inside and outside.  
        5. Explain why Singularity is preferred over Docker in shared HPC.  
        """)

    # -------------------------
    # Drill
    # -------------------------
    with st.expander("❓ Questions — quick Q&A"):
        st.markdown(textwrap.dedent("""
        1. Difference between Docker and Singularity?  
        - Docker needs root, Singularity is rootless and HPC-safe.  

        2. How do you build an image in Docker vs Singularity?  
        - Docker: `docker build -t image .`  
        - Singularity: `singularity build image.sif docker://imagename`.  

        3. How do containers integrate with SLURM?  
        - SLURM job script calls `singularity exec ... python3 script.py`.  

        4. How do you check GPU availability inside a container?  
        - `singularity exec --nv image.sif python3 -c "import torch; print(torch.cuda.is_available())"`.  

        5. Why not just use virtual environments instead of containers?  
        - Containers give reproducibility, isolation, portability across clusters.  
        """))

    st.success("Containerization module loaded — master Docker, Singularity, and HPC integration.")
