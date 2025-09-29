import streamlit as st
import textwrap

def _code(cmd: str, lang="bash"):
    """Helper for clean code blocks"""
    st.code(textwrap.dedent(cmd).strip(), language=lang)

def render():
    st.header("6️⃣ GPU Performance Basics and Optimization")
    st.markdown("""
    Goal: Achieve maximum throughput for your deep learning jobs by mastering GPU monitoring, 
    efficient memory utilization, and modern distributed training techniques.
    """)

    st.markdown("---")

    # -------------------------
    # 1. Real-Time Monitoring & Utilization
    # -------------------------
    st.subheader("1. Real-Time Monitoring & Utilization")
    with st.expander("👁️ Check GPU Status and Processes", expanded=True):
        st.markdown("""
        Use these commands on the compute node where your job is running to diagnose utilization issues and memory leaks.
        """)

        st.markdown("#### Command-Line Monitoring")
        _code("""# Primary tool: Shows utilization, memory, and running processes
nvidia-smi

# Real-time monitoring (replace 1 with the desired refresh rate in seconds)
watch -n 1 nvidia-smi

# If available, 'gpustat' offers a cleaner, single-line overview
gpustat --watch 1
""", language="bash")
        
        st.markdown("#### Key Metrics in `nvidia-smi`")
        st.markdown(textwrap.dedent("""
        - **`Util` (GPU Utilization):** The percentage of time the GPU is actively processing commands. **Aim for >70%** during training.
        - **`Mem` (Memory Usage):** The memory currently allocated by your process. If this hits 100%, your job will crash (OOM error).
        - **`PID` (Process ID):** Shows which process is using the GPU. Use `kill <PID>` to stop a rogue process.
        """))

    st.markdown("---")
    
    # -------------------------
    # 2. Memory & Speed Optimization Strategies
    # -------------------------
    st.subheader("2. Core Optimization Strategies for AI")
    with st.expander("🧪 Techniques to Boost Speed and Save VRAM"):
        
        st.markdown("#### A. Mixed Precision Training (AMP)")
        st.markdown("""
        Modern GPUs (A100/H100) are optimized for **FP16 (half-precision)** and **BFLOAT16**. Using these formats significantly reduces VRAM usage and doubles training speed due to dedicated hardware (Tensor Cores).
        """)
        
        _code("""# PyTorch Automatic Mixed Precision (AMP) is MANDATORY on MBZUAI GPUs
import torch.cuda.amp as amp

# Initialize the gradient scaler
scaler = amp.GradScaler()

# ... training setup ...

with amp.autocast():
    # Model forward pass happens here in mixed precision
    output = model(data)
    loss = criterion(output, target)

# Loss scaling is handled automatically to prevent underflow
scaler.scale(loss).backward()
scaler.step(optimizer)
scaler.update()
""", language="python")

        st.markdown("#### B. Gradient Accumulation")
        st.markdown("""
        If you need a very large effective batch size but lack the VRAM to fit it, use **Gradient Accumulation**. It processes small micro-batches and accumulates the gradients before performing a single optimization step.
        """)
        
        _code("""# Effective Batch Size = Micro Batch Size * Accumulation Steps
ACCUMULATION_STEPS = 4

for i, (data, target) in enumerate(dataloader):
    output = model(data)
    loss = criterion(output, target)
    
    # Scale loss by accumulation steps
    loss = loss / ACCUMULATION_STEPS 
    
    # Backward pass
    loss.backward()

    # Only step the optimizer when accumulation is complete
    if (i + 1) % ACCUMULATION_STEPS == 0:
        optimizer.step()
        optimizer.zero_grad()
""", language="python")

    st.markdown("---")
    
    # -------------------------
    # 3. Multi-GPU Strategies
    # -------------------------
    st.subheader("3. Multi-GPU Training: DDP vs. DataParallel")
    with st.expander("⚖️ Distributed Data Parallel (DDP) is Mandatory"):
        st.markdown("""
        For jobs requiring more than one GPU, **Distributed Data Parallel (DDP)** is the only accepted method. The deprecated `DataParallel` is a massive bottleneck and should be avoided entirely.
        """)
        
        st.markdown("#### Why DDP is Superior (and DP is Banned)")
        st.markdown(textwrap.dedent("""
        | Feature | **DDP (`torch.distributed`)** | **DataParallel (`torch.nn.DataParallel`)** |
        | :--- | :--- | :--- |
        | **Performance** | **Excellent.** Minimal network overhead (InfiniBand optimized). | **Terrible.** Requires heavy data replication, severe CPU bottleneck. |
        | **GPU Usage** | All GPUs are equally utilized. | **GPU 0 is bottlenecked** (used for gradient aggregation). |
        | **Scalability** | Scales efficiently to **multiple nodes**. | Cannot scale beyond a single node. |
        """))

        st.markdown("#### DDP Setup Reminder (Python Snippet)")
        _code("""# Python setup within your DDP script
import torch.distributed as dist

# 1. Initialize process group (using env vars set by SLURM)
dist.init_process_group(backend='nccl') 
local_rank = dist.get_rank() # Current process's rank

# 2. Move model to local GPU
torch.cuda.set_device(local_rank)
model.cuda(local_rank)

# 3. Wrap model
model = torch.nn.parallel.DistributedDataParallel(model, device_ids=[local_rank])
# ... Proceed with training ...
""", language="python")

    st.markdown("---")

    # -------------------------
    # 4. Profiling and Deep Dive Memory Check
    # -------------------------
    st.subheader("4. Deep Dive: Memory and Profiling")
    with st.expander("💾 PyTorch Memory Check and Profiling"):
        
        st.markdown("#### PyTorch Memory Functions (for debugging VRAM issues)")
        st.markdown("""
        Use these functions within your Python script to precisely measure the memory footprint of your model and tensors.
        """)
        
        _code("""import torch

# Check CUDA availability and current device
print(f"CUDA Available: {torch.cuda.is_available()}")
print(f"Device Name: {torch.cuda.get_device_name(0)}")

# Check allocated memory (currently used by tensors)
allocated_bytes = torch.cuda.memory_allocated(0)
print(f"Allocated Memory: {allocated_bytes / (1024**3):.2f} GB")

# Check reserved memory (total memory PyTorch holds onto)
reserved_bytes = torch.cuda.memory_reserved(0)
print(f"Reserved Memory: {reserved_bytes / (1024**3):.2f} GB")

# Clear unused cached memory
torch.cuda.empty_cache()
""", language="python")

        st.markdown("#### PyTorch Profiler (Identifying Bottlenecks)")
        st.markdown("""
        When utilization is low, use the PyTorch profiler to see if your code is **CPU-bound** (e.g., slow data loading) or **GPU-bound** (e.g., slow kernel execution).
        """)
        _code("""import torch.profiler as profiler

# Setup the profiling schedule (warmup steps followed by active recording steps)
with profiler.profile(
    activities=[
        torch.profiler.ProfilerActivity.CPU,
        torch.profiler.ProfilerActivity.CUDA,
    ],
    schedule=profiler.schedule(wait=1, warmup=1, active=3, repeat=1),
    on_trace_ready=profiler.tensorboard_trace_handler('./log/profiler_trace'),
    record_shapes=True,
    profile_memory=True
) as p:
    for step, data in enumerate(dataloader):
        # Perform a single training step
        # ... training step ...
        p.step()
        if step > 5:
            break
            
# Run TensorBoard locally via SSH Tunnel to view results!
# tensorboard --logdir=./log
""", language="python")

    st.success("You are now equipped with the tools and techniques to optimize your AI workloads for peak performance on the MBZUAI HPC cluster!")
