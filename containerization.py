# containerization.py
import streamlit as st
import textwrap

def _code(cmd: str, language="bash"):
    """Helper for clean bash/code blocks"""
    st.code(textwrap.dedent(cmd).strip(), language=language)

def render():
    st.header("3️⃣ Containerization Mastery: From Laptop to HPC")
    st.markdown("""
    Goal: Understand **why and how containers are used in HPC labs** like MBZUAI, 
    and learn the **end-to-end workflow** to run AI workloads inside them with Docker and Apptainer.
    """)

    st.markdown("---")

    # -------------------------
    # The End-to-End Workflow
    # -------------------------
    st.subheader("The AI Research Container Workflow")
    st.markdown("""
    The standard process for researchers is a **two-step journey**:
    1.  **Local Development & Packaging (with Docker 🐳):** You build and test your application and its dependencies in a reproducible environment on your local machine.
    2.  **HPC Deployment & Execution (with Apptainer 📦):** You convert your Docker image into a single, secure `.sif` file and run it on a shared HPC cluster using a job scheduler like SLURM.
    """)
    st.image("https://docs.sanger-dev.org/images/singularity_workflow.png", caption="Container workflow: from Docker build to Apptainer on HPC.")

    st.markdown("---")

    # -------------------------
    # Docker Basics
    # -------------------------
    with st.expander("Step 1: Local Development with Docker 🐳"):
        st.markdown("""
        **Docker** is for developers. It helps you define a perfect environment for your project with a `Dockerfile`.
        """)
        
        st.subheader("Example: Building a PyTorch Container")
        st.markdown("Start by writing your `Dockerfile` to capture all dependencies.")
        _code("""
        # Use an official PyTorch image as the base.
        # This one is built for CUDA 11.8 on Ubuntu 22.04.
        FROM nvcr.io/nvidia/pytorch:23.09-py3

        # Set a working directory inside the container.
        WORKDIR /app

        # Copy your local application code into the container.
        COPY . /app/

        # Install any additional libraries your code needs.
        # Here, we're installing a package from PyPI.
        RUN pip install transformers

        # Set the default command to run when the container starts.
        CMD ["python", "train.py"]
        """, language="Dockerfile")

        st.markdown("**Build and Run Locally**")
        st.markdown("After saving the file, use these commands to build and run it on your machine:")
        _code("""
        # Build the image from the Dockerfile.
        docker build -t my-ai-app .

        # Run the container locally. You can test it on your host.
        docker run --rm -it my-ai-app
        """)

    st.markdown("---")

    # -------------------------
    # Singularity / Apptainer
    # -------------------------
    with st.expander("Step 2: HPC Deployment with Apptainer 📦"):
        st.markdown("""
        **Apptainer (formerly Singularity)** is for HPC. It's designed to run containers securely and seamlessly on multi-user systems. It converts your Docker image into a single `.sif` file.
        """)
        
        st.subheader("Converting the Docker Image")
        st.markdown("First, you need to pull and convert your Docker image into a `.sif` file. This is typically done on an HPC login node or a dedicated build machine.")
        _code("""
        # Convert the Docker image you just built into a .sif file.
        # The 'docker-daemon' prefix tells Apptainer to use your local Docker images.
        apptainer build my-ai-app.sif docker-daemon://my-ai-app:latest
        """)

        st.subheader("Running the Container on the HPC")
        st.markdown("Now, you can run the `.sif` file on the cluster. It's a single, portable executable.")
        _code("""
        # Run a command inside the container. The '--nv' flag is crucial for NVIDIA GPU access!
        apptainer exec --nv my-ai-app.sif python3 /app/test_gpu.py
        """)
        st.markdown("""
        > **Note:** The `--nv` flag is what allows the container to see the host's NVIDIA drivers and CUDA libraries.
        """)

    st.markdown("---")

    # -------------------------
    # HPC Integration with SLURM
    # -------------------------
    with st.expander("Step 3: Submitting a SLURM Job with Apptainer ⚡"):
        st.markdown("""
        The final step is to put your Apptainer command inside a SLURM job script to run your workload on the compute nodes.
        """)
        
        st.subheader("Example SLURM Script (`run_job.sh`)")
        st.markdown("This script requests resources and executes your containerized application.")
        _code("""
        #!/bin/bash
        #SBATCH --job-name=containerized_ai
        #SBATCH --account=your_hpc_account  # Replace with your account name
        #SBATCH --partition=gpu
        #SBATCH --nodes=1
        #SBATCH --ntasks-per-node=1
        #SBATCH --cpus-per-task=8
        #SBATCH --gres=gpu:1
        #SBATCH --time=01:00:00
        #SBATCH --output=slurm-%j.out
        #SBATCH --error=slurm-%j.err

        # Execute your containerized Python script.
        # --nv binds the NVIDIA libraries.
        # --bind is used to mount host directories (e.g., your data folder).
        apptainer exec --nv my-ai-app.sif python /app/train.py --data_path /path/to/data
        """)

        st.markdown("**Submitting Your Job**")
        st.markdown("Submit the job to the cluster scheduler:")
        _code("""
        sbatch run_job.sh
        """)

    st.markdown("---")

    # -------------------------
    # Exercises & Q&A
    # -------------------------
    with st.expander("📝 Exercises & Quick Q&A"):
        st.subheader("Exercises")
        st.markdown("""
        1.  Build a Docker image that includes a specific version of a library (e.g., `transformers==4.30.0`).
        2.  Write a Python script that checks the version of that library and include it in your container.
        3.  Convert the Docker image to a `.sif` file.
        4.  Write and submit a SLURM script to run the version-check script inside the container.
        5.  **Bonus:** Try to mount a local data directory into the container using the `--bind` flag in your `apptainer exec` command.
        """)
        st.subheader("Quick Q&A")
        st.markdown(textwrap.dedent("""
        1.  **Why Docker locally, but Apptainer on HPC?**
            - Docker needs a root-owned daemon, which is a security risk on shared HPC systems. Apptainer is designed to run securely and rootlessly.
        2.  **How do I get GPU access inside the container?**
            - You use the `--gpus all` flag with Docker and the `--nv` flag with Apptainer.
        3.  **What is a `.sif` file?**
            - A **S**ingularity **I**mage **F**ormat file. It's a single, self-contained, and immutable file that bundles your entire container environment.
        4.  **Why use containers over virtual environments like Conda?**
            - Containers include the entire OS, making them portable and fully reproducible across different clusters. Conda environments can still fail due to underlying OS differences.
        """))
    st.success("You are now equipped to containerize and deploy your AI workloads on an HPC cluster. 🚀")
