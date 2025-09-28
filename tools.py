# tools.py
import streamlit as st
import textwrap

def render():
    st.header("🛠️ HPC Tools — Container & SLURM Script Generator")

    st.markdown("""
    These tools are designed for **MBZUAI’s Campus Supercomputing Center (CSCC)**,  
    powered by **HPE Apollo 6500 Gen10 Plus** with **AMD EPYC CPUs** and **384 NVIDIA A100 GPUs**.
    """)

    # Tabs for tools
    tab1, tab2 = st.tabs(["📦 Container Generator", "📜 SLURM Script Generator"])

    # ------------------------
    # Container Generator
    # ------------------------
    with tab1:
        st.subheader("📦 Container Generator")
        st.markdown("Generate a **Dockerfile** or **Singularity definition** for AI/ML workloads.")

        container_type = st.radio("Select container type:", ["Dockerfile", "Singularity"])
        base_image = st.text_input("Base image (e.g., pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime)")
        install_libs = st.text_area("Python libraries to install (space-separated)", "numpy pandas matplotlib torch torchvision opencv-python")
        entry_cmd = st.text_input("Default command", "python3")

        if st.button("Generate Container Spec"):
            if container_type == "Dockerfile":
                dockerfile = f"""
                FROM {base_image}

                # Install extra libraries
                RUN pip install {install_libs}

                # Set working directory
                WORKDIR /workspace

                # Default command
                CMD ["{entry_cmd}"]
                """
                dockerfile = textwrap.dedent(dockerfile)
                st.code(dockerfile, language="dockerfile")
                st.copy_button("📋 Copy Dockerfile", dockerfile)

            else:  # Singularity
                singularity = f"""
                Bootstrap: docker
                From: {base_image}

                %post
                    apt-get update && apt-get install -y python3-pip
                    pip install {install_libs}

                %runscript
                    exec {entry_cmd} "$@"
                """
                singularity = textwrap.dedent(singularity)
                st.code(singularity, language="bash")
                st.copy_button("📋 Copy Singularity Definition", singularity)

    # ------------------------
    # SLURM Script Generator
    # ------------------------
    with tab2:
        st.subheader("📜 SLURM Script Generator")
        st.markdown("Generate a **custom job script** for MBZUAI’s SLURM system on **A100 GPUs**.")

        # User inputs
        job_name = st.text_input("Job Name", "ai_training_job")
        time = st.text_input("Walltime (HH:MM:SS)", "02:00:00")
        gpus = st.number_input("Number of GPUs", 1, 8, 1)
        cpus = st.number_input("Number of CPUs per task", 1, 64, 8)
        mem = st.text_input("Memory (e.g., 64G)", "64G")
        partition = st.text_input("Partition/queue (if known)", "gpu")
        script_name = st.text_input("Script to run", "train.py")

        if st.button("Generate SLURM Script"):
            slurm_script = f"""
            #!/bin/bash
            #SBATCH --job-name={job_name}
            #SBATCH --gres=gpu:{gpus}
            #SBATCH --cpus-per-task={cpus}
            #SBATCH --time={time}
            #SBATCH --mem={mem}
            #SBATCH --partition={partition}
            #SBATCH --output=slurm-%j.out

            # Load required modules
            module load python/3.10
            module load cuda/11.8

            # Print debug info
            echo "Job started on $(date)"
            echo "Running on node $(hostname)"
            echo "Using {gpus} A100 GPU(s) and {cpus} CPU(s)"

            # Run program
            python3 {script_name}

            echo "Job finished on $(date)"
            """
            slurm_script = textwrap.dedent(slurm_script)
            st.code(slurm_script, language="bash")
            st.copy_button("📋 Copy SLURM Script", slurm_script)

    st.info("✅ Tip: Copy the generated files and paste them into your HPC environment.")
