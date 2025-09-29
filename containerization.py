# containerization.py
import streamlit as st
import textwrap

def _code(cmd: str, language="bash"):
    """Helper for clean bash/code blocks"""
    st.code(textwrap.dedent(cmd).strip(), language=language)

def render():
    st.header("📦 Containerization Mastery: From Local to HPC")
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

    # -------------------------
    # List of Commands
    # -------------------------
    st.markdown("---")
    st.header("Docker vs. Apptainer: Command Reference")

    st.markdown("""
    Here is an extensive list of common Docker and Apptainer commands. While they serve a similar purpose of managing containers, their command-line interfaces and underlying philosophies differ significantly. Docker is focused on microservices and multi-user environments, while Apptainer (formerly Singularity) is optimized for high-performance computing (HPC) environments and scientific research, prioritizing a single-user, secure model.
    """)

    st.markdown("---")

    st.subheader("Docker Commands")
    st.markdown("Docker commands are generally structured as `docker [command] [options]`.")

    st.markdown("#### **Image Management**")
    _code("""
    docker pull [image_name]              # Downloads an image from a registry
    docker build -t [image_name]:[tag] .  # Builds a new image from a Dockerfile
    docker images                         # Lists all local Docker images
    docker rmi [image_id]                 # Removes one or more images
    docker push [image_name]              # Uploads a local image to a registry
    docker search [search_term]           # Searches for images on Docker Hub
    """)

    st.markdown("#### **Container Lifecycle**")
    _code("""
    docker run [options] [image_name] [command]   # Creates and starts a new container
    docker ps                                     # Lists all running containers
    docker ps -a                                  # Lists all containers (including stopped)
    docker start [container_id/name]              # Starts a stopped container
    docker stop [container_id/name]               # Gracefully stops a running container
    docker kill [container_id/name]               # Forcibly stops a running container
    docker rm [container_id/name]                 # Removes a stopped container
    docker exec -it [container_id/name] [command] # Executes a command inside a running container
    docker logs [container_id/name]               # Fetches the logs of a container
    """)

    st.markdown("#### **System and Cleanup**")
    _code("""
    docker info             # Displays system-wide Docker information
    docker system prune     # Removes unused containers, networks, images, etc.
    docker volume ls        # Lists all Docker volumes
    docker network ls       # Lists all Docker networks
    """)
    st.markdown("---")

    st.subheader("Apptainer Commands")
    st.markdown("Apptainer commands are generally structured as `apptainer [command] [options]`.")

    st.markdown("#### **Image Management**")
    _code("""
    apptainer build [sif_file_name] [source_uri]              # Builds a new SIF image
    apptainer pull [sif_file_name] [source_uri]               # Downloads and converts an image
    apptainer push [sif_file_name] [destination_uri]          # Uploads a SIF image to a registry
    apptainer inspect [sif_file_name]                         # Displays metadata about a SIF image
    apptainer verify [sif_file_name]                          # Verifies the digital signature of an image
    """)

    st.markdown("#### **Container Execution**")
    _code("""
    apptainer run [sif_file_name] [args]          # Executes the default runscript inside the image
    apptainer shell [sif_file_name]               # Gives you an interactive shell inside the container
    apptainer exec [sif_file_name] [command]      # Executes a command inside the container
    apptainer instance start [sif_file_name] [instance_name] # Runs a container as a long-running service
    apptainer instance list                       # Lists all currently running Apptainer instances
    apptainer instance stop [instance_name]       # Stops a named Apptainer instance
    """)

    st.markdown("#### **Security and Networking**")
    _code("""
    apptainer sign [sif_file_name]                # Cryptographically signs a SIF image
    apptainer remote                              # Manages remote registries and keyservers
    apptainer oci                                 # Works with OCI-compliant images (like Docker)
    """)
    st.markdown("---")

    st.header("Dockerfile: The Blueprint for a Container")
    st.markdown("""
    A **Dockerfile** is a text file that contains a series of instructions for Docker to build a **Docker image**. Each instruction creates a new layer on top of the previous one, defining the complete environment—from the operating system to the application code and dependencies.
    """)
    st.markdown("#### **Core Dockerfile Instructions**")
    st.markdown(textwrap.dedent("""
    - **`FROM [image]:[tag]`**: Specifies the **base image** for the build. This must be the first instruction.
    - **`RUN [command]`**: Executes a command inside the container during the image build. This is used to install software.
    - **`COPY [source] [destination]`**: Copies files from your local machine (the build context) into the container image.
    - **`WORKDIR [path]`**: Sets the **working directory** for all subsequent instructions.
    - **`CMD ["executable", "param1", "param2"]`**: Provides **default arguments** for an executing container. This is overridden by a command on `docker run`.
    - **`ENTRYPOINT ["executable", "param1", "param2"]`**: Configures the container to run as a specific **executable**. It is not overridden by `docker run` but instead, the command is appended as arguments.
    - **`ENV [key] [value]`**: Sets an **environment variable** inside the container.
    - **`EXPOSE [port]`**: Informs Docker that the container listens on the specified network ports at runtime.
    - **`LABEL [key]="[value]"`**: Adds **metadata** to an image.
    """))

    st.markdown("#### **Example Dockerfile**")
    _code("""
    # Use a lightweight official Python base image
    FROM python:3.9-slim

    # Set an environment variable
    ENV PYTHONUNBUFFERED=1

    # Set the working directory
    WORKDIR /app

    # Copy the requirements file and install dependencies
    COPY requirements.txt .
    RUN pip install -r requirements.txt

    # Copy the application code
    COPY . .

    # Expose a port (for documentation)
    EXPOSE 5000

    # Run the application
    CMD ["python", "app.py"]
    """, language="Dockerfile")
