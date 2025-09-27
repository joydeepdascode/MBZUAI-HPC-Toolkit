import streamlit as st

def render():
    st.header("⚡ GPU Performance Basics")
    st.markdown("""
    **Monitor & Optimize GPU usage:**
    
    - `nvidia-smi` → check utilization, memory
    - `watch -n 1 nvidia-smi` → real-time monitoring
    - PyTorch profiling: `torch.cuda.max_memory_allocated()`
    - Multi-GPU training: `torch.nn.DataParallel` or `torch.distributed`
    
    **Tips:**
    - Minimize data transfer between CPU/GPU
    - Use mixed precision (`torch.cuda.amp`)
    """)

    st.subheader("Check GPU Memory in PyTorch")
    st.code("""import torch

print(torch.cuda.is_available())
print(torch.cuda.get_device_name(0))
print(torch.cuda.memory_allocated(0))
print(torch.cuda.memory_reserved(0))
""", language="python")
