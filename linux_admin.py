import streamlit as st

def render():
    st.header("🐧 Linux Administration")

    # -------------------------------
    # Users and Groups
    # -------------------------------
    st.subheader("Users and Groups")
    st.markdown("""
    - File containing users: **`/etc/passwd`**  
    - File containing groups: **`/etc/group`**
    """)
    st.code("cut -d: -f1 /etc/passwd", language="bash")

    st.subheader("Check Current User & Groups")
    st.code("""whoami   # Current username
groups   # Groups of current user
id       # UID, GID, and groups in detail
""", language="bash")

    st.subheader("Creating Users")
    st.code("""sudo useradd -m -d /home/students/hpcuser1 -s /bin/bash hpcuser1
sudo adduser --home /home/students/hpcuser1 --shell /bin/bash hpcuser1
""", language="bash")

    st.subheader("Deleting Users")
    st.code("""sudo userdel -r username
sudo deluser --remove-home username
""", language="bash")

    st.subheader("Managing Groups")
    st.code("""sudo usermod -aG <group> <user>
sudo gpasswd -d <user> <group>
sudo usermod -G group1,group2 user
sudo groupadd researchers
sudo groupdel researchers
getent group
""", language="bash")

    st.subheader("📝 Exercise: Users & Groups")
    st.markdown("""
    1. Create a user `hpcstudent`.  
    2. Create a group `cpugroup`.  
    3. Add `hpcstudent` to `cpugroup`.  
    4. Verify UID, GID, and groups.  
    5. Change password for `hpcstudent`.  
    6. Remove `hpcstudent` and verify deletion.  
    """)

    # -------------------------------
    # Ownership & Permissions
    # -------------------------------
    st.subheader("Ownership (`chown`, `chgrp`)")
    st.code("""sudo chown user:group /tmp/script.sh
sudo chown user:group /tmp/hpc_demo
sudo chgrp researchers /tmp/hpc_demo
""", language="bash")

    st.subheader("Modes & Permissions (`chmod`, `umask`)")
    st.code("""sudo chmod 770 file.sh
sudo chmod 2770 /tmp/hpc_workshop1   # setgid + group perms
sudo chmod 4755 /tmp/file.sh         # suid
umask 022
""", language="bash")

    st.markdown("""
    - Default: files `666`, dirs `777`  
    - With `umask 022`:  
      - Files → `644` (`rw-r--r--`)  
      - Dirs → `755` (`rwxr-xr-x`)  
    """)

    # -------------------------------
    # Services
    # -------------------------------
    st.subheader("Managing Services (systemd)")
    st.code("""sudo systemctl status ssh
sudo systemctl start slurmd
sudo systemctl stop slurmd
sudo systemctl restart ssh
sudo systemctl enable ssh
""", language="bash")

    # -------------------------------
    # Processes
    # -------------------------------
    st.subheader("Processes & Monitoring")
    st.code("""ps aux | head -n 20   # List processes
top                     # Live monitor
htop                    # Interactive monitor
""", language="bash")

    st.subheader("Process Control & Priorities")
    st.code("""kill <pid>
pkill <name>

nice -n 10 my_job &
renice +10 -p PID
sudo renice -n -10 -p PID
""", language="bash")

    # -------------------------------
    # Disk & Storage
    # -------------------------------
    st.subheader("💾 Disk & Storage")
    st.markdown("""
    Monitor and manage storage:
    """)
    st.code("""df -h        # Disk usage by filesystem
du -sh *     # Size of directories/files
lsblk        # Block devices
mount        # Mounted filesystems
iostat       # I/O statistics
""", language="bash")

    st.subheader("📝 Practice: Disk & Storage")
    st.markdown("""
    1. Check disk usage with `df -h`.  
    2. Find which folder is largest using `du -sh *`.  
    3. List all block devices with `lsblk`.  
    4. Mount a directory manually using `mount`.  
    5. Simulate a “disk full” scenario by creating a large dummy file with `dd`.  
    """)

    # -------------------------------
    # Logs & Troubleshooting
    # -------------------------------
    st.subheader("📜 Logs & Troubleshooting")
    st.markdown("""
    System logs are critical for debugging:
    """)
    st.code("""journalctl -xe            # Systemd logs
dmesg | tail -n 20      # Kernel messages
cat /var/log/syslog     # System logs (Debian/Ubuntu)
cat /var/log/messages   # System logs (RHEL/CentOS)
""", language="bash")

    st.subheader("📝 Practice: Logs")
    st.markdown("""
    1. Use `journalctl -xe` to check for errors.  
    2. Use `dmesg` to see hardware/kernel issues.  
    3. Explore `/var/log/syslog` and `/var/log/messages` and describe differences.  
    """)

    # -------------------------------
    # Networking Basics
    # -------------------------------
    st.subheader("🌐 Networking Basics")
    st.markdown("""
    Check and troubleshoot network connectivity:
    """)
    st.code("""ip a              # List interfaces
ping 8.8.8.8      # Test connectivity
ss -tulnp         # Show listening sockets
netstat -tulnp    # Alternative (legacy)
""", language="bash")

    st.subheader("📝 Practice: Networking")
    st.markdown("""
    1. List all network interfaces with `ip a`.  
    2. Test connectivity with `ping google.com`.  
    3. Check which services are listening with `ss -tulnp`.  
    4. Verify open ports using `netstat`.  
    """)
