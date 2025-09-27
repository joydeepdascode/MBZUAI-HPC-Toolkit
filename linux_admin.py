import streamlit as st

def render():
    st.header("🐧 Linux Administration")

    # Section: Users and Groups
    st.subheader("Users and Groups")
    st.markdown("""
    - File containing users: **`/etc/passwd`**  
    - File containing groups: **`/etc/group`**

    Example: List all users from `/etc/passwd`:
    """)
    st.code("cut -d: -f1 /etc/passwd", language="bash")

    st.markdown("""
    - `cut` → extracts info from file  
    - `-d:` → delimiter `:`  
    - `-f1` → first field  
    """)

    # Check current user and groups
    st.subheader("Check Current User & Groups")
    st.code("""whoami   # Current username
groups   # Groups of current user
id       # UID, GID, and groups in detail
""", language="bash")

    # Creating Users
    st.subheader("Creating Users")
    st.markdown("**Low-level:** `useradd`")
    st.code("""# Add user with home directory and shell
sudo useradd -m -d /home/students/hpcuser1 -s /bin/bash hpcuser1
""", language="bash")

    st.markdown("**High-level:** `adduser`")
    st.code("""sudo adduser --home /home/students/hpcuser1 --shell /bin/bash hpcuser1
""", language="bash")

    # Deleting Users
    st.subheader("Deleting Users")
    st.code("""sudo userdel -r username         # delete user + home + mail spool
sudo deluser --remove-home username
""", language="bash")

    # Group Management
    st.subheader("Managing Groups")
    st.code("""# Add user to a group
sudo usermod -aG <group> <user>

# Remove user from group
sudo gpasswd -d <user> <group>

# Assign all groups
sudo usermod -G group1,group2,group3 user
""", language="bash")

    st.code("""# Create group
sudo groupadd researchers

# Delete group
sudo groupdel researchers

# List groups
getent group
""", language="bash")

    # Exercise
    st.subheader("📝 Exercise")
    st.markdown("""
    1. Create a user `hpcstudent`.  
    2. Create a group `cpugroup`.  
    3. Add `hpcstudent` to `cpugroup`.  
    4. Verify UID, GID, and groups of `hpcstudent`.  
    5. Change password for `hpcstudent`.  
    6. Remove `hpcstudent` and verify deletion.  
    """)

    # Quick Recap
    st.subheader("❓ Quick Recap (Interview Drill)")
    st.markdown("""
    1. How do you list all users?  
    2. How do you list all groups?  
    3. How do you check your current UID, GID, and groups?  
    4. How do you create a user with a custom home directory?  
    5. How do you append a user to a group?  
    6. How do you remove a user along with their home directory?  
    7. How do you change a user’s password?  
    """)

    # Ownership
    st.subheader("Ownership (`chown`, `chgrp`)")
    st.code("""# Change ownership of file
sudo chown user:group /tmp/script.sh

# Change ownership of directory
sudo chown user:group /tmp/hpc_demo

# Change group only
sudo chgrp researchers /tmp/hpc_demo
""", language="bash")

    # Permissions
    st.subheader("Modes & Permissions (`chmod`, `umask`)")
    st.code("""# Change file permissions
sudo chmod 770 file.sh

# Set group inheritance on directory
sudo chmod 2770 /tmp/hpc_workshop1

# Set SUID on file
sudo chmod 4755 /tmp/file.sh
""", language="bash")

    st.markdown("""
    **umask example:**  
    Default permissions: files `666`, dirs `777`  
    With `umask 022`:  
    - Files → `644` (`rw-r--r--`)  
    - Dirs → `755` (`rwxr-xr-x`)  
    """)

    # Services
    st.subheader("Managing Services (systemd)")
    st.code("""# Service management
sudo systemctl status ssh
sudo systemctl start slurmd
sudo systemctl stop slurmd
sudo systemctl restart ssh
sudo systemctl enable ssh
""", language="bash")

    # Processes
    st.subheader("Processes & Monitoring")
    st.code("""ps aux | head -n 20   # List processes
top                     # Live system monitor
htop                    # Interactive monitor
""", language="bash")

    # Kill / Priorities
    st.subheader("Process Control & Priorities")
    st.code("""kill <pid>           # Kill process
pkill <name>           # Kill by name

# Priority with nice/renice
nice -n 10 my_cpu_job_command &
renice +10 -p PID
sudo renice -n -10 -p PID
""", language="bash")
