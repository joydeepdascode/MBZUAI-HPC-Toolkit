import streamlit as st

def render():
    st.header("🐧 Linux Administration")
    st.markdown("""
    **Core Linux Admin tasks for AI/HPC workflows:**
    
    - **Users & Groups:** `useradd`, `usermod`, `groupadd`
    - **File Permissions:** `chmod`, `chown`, `umask`
    - **Package Management:** `apt`, `yum`, `pip`
    - **System Monitoring:** `top`, `htop`, `nvidia-smi`, `df -h`
    - **Networking:** `ssh`, `scp`, `rsync`
    - **Process Management:** `ps`, `kill`, `nice`, `renice`
    """)

    st.subheader("Mini Exercise: Check GPU & Disk")
    st.code("""# Check NVIDIA GPU status
nvidia-smi

# Check disk usage
df -h
""", language="bash")
