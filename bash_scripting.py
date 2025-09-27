import streamlit as st

def render():
    st.header("📜 Bash Scripting")
    st.markdown("""
    Automate AI/HPC tasks with **Bash scripts**:

    - Script header: `#!/bin/bash`
    - Variables & Loops
    - Conditionals (`if`, `case`)
    - Functions & Logging
    - Error Handling (`set -e`, `trap`)
    """)

    st.subheader("Example: Loop to run training scripts")
    st.code("""#!/bin/bash
for lr in 0.001 0.01 0.1
do
    python train_model.py --learning_rate $lr
done
""", language="bash")
