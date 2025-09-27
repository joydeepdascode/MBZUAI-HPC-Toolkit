import streamlit as st

def render():
    st.header("🐳 Containerization")
    st.markdown("""
    Use Docker/Singularity to run reproducible AI experiments:

    **Docker Example:**
    - Base image: `nvidia/cuda:12.1-base`
    - Install PyTorch, OpenCV, etc.

    **Singularity Example:**
    - Convert Docker to Singularity for HPC clusters
    - `singularity build mycontainer.sif docker://image_name`
    """)

    st.subheader("Dockerfile Template for AI Workflows")
    st.code("""FROM nvidia/cuda:12.1-cudnn8-runtime-ubuntu22.04

# Install dependencies
RUN apt-get update && apt-get install -y python3 python3-pip git
RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
RUN pip3 install opencv-python matplotlib jupyter

WORKDIR /workspace
CMD ["/bin/bash"]
""", language="docker")
