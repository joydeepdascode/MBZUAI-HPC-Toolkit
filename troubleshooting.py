import streamlit as st

def render():
    st.header("🔧 Troubleshooting Techniques for AI/HPC")
    st.markdown("""
    **Common Issues & Fixes:**

    - **Job fails in SLURM:** check `error.log`, `scontrol show job <jobid>`
    - **Out of GPU memory:** reduce batch size, use `torch.cuda.empty_cache()`
    - **Container issues:** verify image with `docker run -it image /bin/bash`
    - **Dependency conflicts:** use virtualenv or conda
    - **Network/File access issues:** check `ssh`, `rsync`, `permissions`
    """)

    st.subheader("Example: Clear GPU Memory in PyTorch")
    st.code("""import torch

torch.cuda.empty_cache()
print("GPU memory cleared")
""", language="python")
