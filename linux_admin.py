# linux_admin.py
import streamlit as st
import textwrap

def _code(cmd: str):
    """Helper to show a bash code block with cleaned indentation."""
    st.code(textwrap.dedent(cmd).strip(), language="bash")

def render():
    st.header("🐧 Linux Administration — Practical Guide")
    st.markdown("A compact, copy-friendly reference for user/group management, permissions, services, storage, logs and networking.")

    # -------------------------
    # Users & Groups (Files)
    # -------------------------
    with st.expander("📁 Users & Groups — files (/etc/passwd, /etc/group)"):
        st.markdown("""
        - Users live in **`/etc/passwd`**  
        - Groups live in **`/etc/group`**
        - Example: list all usernames from `/etc/passwd`
        """)
        _code("cut -d: -f1 /etc/passwd")

        st.markdown("**What the command parts mean:**")
        st.markdown("- `cut` -> extract fields from a file\n- `-d:` -> use `:` as delimiter\n- `-f1` -> print first field")

    # -------------------------
    # Current user & groups
    # -------------------------
    with st.expander("👤 Check current user & groups"):
        st.markdown("Quick commands to check who you are and which groups you belong to.")
        _code("""whoami      # current username
groups      # show groups for current user
id          # UID, GID and group membership details""")

    # -------------------------
    # User Management
    # -------------------------
    with st.expander("🔧 User Management (create / delete / modify)"):
        st.markdown("**Low-level vs high-level**: `useradd`/`userdel` are low-level; `adduser`/`deluser` are friendlier wrappers on many distros.")
        st.subheader("Create user — examples")
        _code("""# Low level (create home, set shell)
sudo useradd -m -d /home/students/hpcuser1 -s /bin/bash hpcuser1

# High level (interactive)
sudo adduser --home /home/students/hpcuser1 --shell /bin/bash hpcuser1
""")

        st.subheader("Delete user — examples")
        _code("""# Remove user + home + mail spool (userdel)
sudo userdel -r username

# Equivalent high-level command
sudo deluser --remove-home username
""")

        st.subheader("Change password")
        _code("sudo passwd <username>")

        st.subheader("Modify groups / membership")
        _code("""# Append user to group (safe: -aG)
sudo usermod -aG <group-name> <user-name>

# Remove user from a group
sudo gpasswd -d <user-name> <group-name>

# Replace all supplementary groups for a user (use carefully)
sudo usermod -G group1,group2 <user-name>
""")

        st.markdown("**Interactive: generate commands for a username/group**")
        username = st.text_input("Username", value="hpcstudent", key="user_name_input")
        home_dir = st.text_input("Home directory", value=f"/home/{username}", key="user_home_input")
        shell = st.text_input("Shell", value="/bin/bash", key="user_shell_input")
        groupname = st.text_input("Group name", value="cpugroup", key="group_name_input")

        if st.button("Show create/add/delete commands"):
            st.write("Create (low-level):")
            _code(f"sudo useradd -m -d {home_dir} -s {shell} {username}")
            st.write("Create (high-level):")
            _code(f"sudo adduser --home {home_dir} --shell {shell} {username}")
            st.write("Create group:")
            _code(f"sudo groupadd {groupname}")
            st.write("Add user to group:")
            _code(f"sudo usermod -aG {groupname} {username}")
            st.write("Verify UID/GID/groups:")
            _code(f"id {username}")
            st.write("Change password:")
            _code(f"sudo passwd {username}")
            st.write("Delete user and remove home:")
            _code(f"sudo userdel -r {username}")
            st.info("Commands that modify users/groups require sudo/root.")

    # -------------------------
    # Groups & listing
    # -------------------------
    with st.expander("👥 Groups (create/list/delete)"):
        _code("""# Add new group (low level)
sudo groupadd <group-name>

# Alternative high-level
sudo addgroup <group-name>

# Delete group
sudo groupdel <group-name>

# List groups from system DB
getent group
""")

    # -------------------------
    # Ownership & Permissions
    # -------------------------
    with st.expander("🔐 Ownership & Permissions (chown, chgrp, chmod, umask)"):
        st.markdown("Change owner/group and control permissions. Numeric modes are commonly used.")
        _code("""# Change ownership of file/directory
sudo chown user:group /tmp/script.sh
sudo chown -R user:group /path/to/dir

# Change group only
sudo chgrp researchers /tmp/hpc_demo

# Change permission bits (example)
sudo chmod 770 file.sh
""")
        st.subheader("Setgid on directory (new files inherit directory's group)")
        _code("sudo chmod 2770 /tmp/hpc_workshop1  # setgid bit + rwxrwx---")
        st.subheader("Make a file setuid (runs with file owner's privileges)")
        _code("sudo chmod 4755 /tmp/file.sh  # careful: security implications")

        st.subheader("umask — default permission mask")
        st.markdown(textwrap.dedent("""
        - System default creation modes: files `666` (rw-rw-rw-), dirs `777` (rwxrwxrwx).
        - `umask` subtracts bits. Example:
          - `umask 022` -> files: 666-022 = 644 (rw-r--r--), dirs: 777-022 = 755 (rwxr-xr-x)
        """))
        _code("umask  # display current mask\numask 022  # set mask (session-only unless in shell rc)")

        st.markdown("**Interactive chmod generator**")
        perm = st.text_input("Enter numeric mode (e.g., 2755, 770, 644)", value="770", key="chmod_input")
        path = st.text_input("File / directory path", value="/tmp/example", key="chmod_path_input")
        if st.button("Show chmod command"):
            _code(f"sudo chmod {perm} {path}")

    # -------------------------
    # Systemd / Services
    # -------------------------
    with st.expander("⚙️ Services (systemd)"):
        st.markdown("Common management commands for systemd services.")
        _code("""# Check status
sudo systemctl status ssh

# Start / stop / restart
sudo systemctl start slurmd
sudo systemctl stop slurmd
sudo systemctl restart ssh

# Enable/disable on boot
sudo systemctl enable ssh
sudo systemctl disable slurmd

# Check active state
sudo systemctl is-active ssh
""")

    # -------------------------
    # Processes & Scheduling
    # -------------------------
    with st.expander("🖥 Processes, Monitoring & Priority"):
        _code("""# Snapshot of processes (top lines)
ps aux | head -n 20

# Live monitors
top
htop   # (may need install: sudo apt install htop)

# Kill / pkill
kill <pid>
pkill <process-name>

# Set priority (niceness)
nice -n 10 my_cpu_job_command &
renice +10 -p <PID>          # increase niceness (lower priority)
sudo renice -n -10 -p <PID>  # reduce niceness (raise priority) - needs sudo
""")
        st.markdown("**Tip:** Use `sudo` for operations requiring elevated privileges. Observe system impact when changing niceness or killing processes.")

    # -------------------------
    # Disk & Storage
    # -------------------------
    with st.expander("💾 Disk & Storage"):
        st.markdown("Commands to inspect and manage disks and mountpoints.")
        _code("""df -h           # disk usage by filesystem (human readable)
du -sh *         # size of files/directories in current path
lsblk            # block devices tree
mount            # show mounted filesystems
iostat -x 1 2    # I/O stats (sysstat package)""")
        st.markdown("**Mount example (read-only loop mount of an ISO):**")
        _code("""sudo mount -o loop image.iso /mnt/iso -t iso9660  # if you have an ISO file""")

        st.subheader("Simulate a 'disk full' safely (use a tmpfs to avoid damaging real disks)")
        st.markdown(textwrap.dedent("""
        1. Create a small RAM-backed filesystem (tmpfs) for experimentation.
        2. Fill tmpfs with a file until full. tmpfs is destroyed on reboot — safe for testing.
        """))
        _code("""# Create a 50MB tmpfs
sudo mkdir -p /mnt/tmpfs_test
sudo mount -t tmpfs -o size=50M tmpfs /mnt/tmpfs_test

# Fill it (careful!)
dd if=/dev/zero of=/mnt/tmpfs_test/bigfile bs=1M count=60  # this will hit "no space" around 50MB
# After test, unmount and remove
sudo umount /mnt/tmpfs_test
sudo rmdir /mnt/tmpfs_test
""")
        st.warning("Don't run destructive commands on production disks. Use tmpfs or allocated test volumes.")

        st.markdown("**Note:** `iostat` is part of `sysstat` — install with `sudo apt install sysstat` on Debian/Ubuntu.")

    # -------------------------
    # Logs & Troubleshooting
    # -------------------------
    with st.expander("📜 Logs & Troubleshooting"):
        st.markdown("System and kernel logs — essential for debugging hardware, services, and boot-time issues.")
        _code("""journalctl -xe              # recent systemd logs with priority and explanatory output
journalctl -u slurmd -n 200   # recent logs for slurmd unit
dmesg | tail -n 50            # kernel ring buffer (hardware / boot messages)
dmesg | grep -i -E "error|fail|warn"  # filter kernel messages

# Traditional log files
sudo tail -n 200 /var/log/syslog      # Debian/Ubuntu system messages
sudo tail -n 200 /var/log/messages    # RHEL/CentOS system messages (if present)
""")
        st.subheader("Practice: reading logs")
        st.markdown(textwrap.dedent("""
        1. `journalctl -xe` -> find recent errors (journal is structured, useful for service units).
        2. `dmesg` -> look for disk, PCI, GPU or driver related errors during boot or plug events.
        3. Inspect `/var/log/syslog` vs `/var/log/messages`: distribution-dependent; both hold system messages, `/var/log/messages` more common in RHEL-family.
        """))

    # -------------------------
    # Networking Basics
    # -------------------------
    with st.expander("🌐 Networking Basics"):
        st.markdown("Inspect interfaces, test connectivity, and view listening sockets.")
        _code("""ip a                # list interfaces and addresses
ip route            # routing table
ping 8.8.8.8        # connectivity test (Ctrl+C to stop)
ss -tulnp           # show listening sockets with process info
netstat -tulnp      # legacy alternative (may need net-tools package)
""")
        st.subheader("Practice tasks")
        st.markdown(textwrap.dedent("""
        1. `ip a` — confirm interface state (UP/DOWN) and addresses.  
        2. `ping google.com` — DNS + connectivity test.  
        3. `ss -tulnp` — see which services are listening and the owning PIDs.  
        4. `ip route` — check default gateway.
        """))

    # -------------------------
    # Quick Exercises (Users had asked)
    # -------------------------
    with st.expander("📝 Exercises (execute on a test VM)"):
        st.markdown("""
        1. Create a user `hpcstudent` and a group `cpugroup`, add the user to the group, confirm with `id hpcstudent`.
        2. Change `hpcstudent`'s password with `sudo passwd hpcstudent`.
        3. Create a tmpfs, simulate disk-full with `dd`, then clean up.
        4. Use `journalctl -u slurmd -n 100` and `dmesg` to look for hardware or driver errors.
        5. Use `ip a`, `ping`, and `ss -tulnp` to diagnose network reachability and open services.
        """)
        _code("""# Quick scripted sequence (replace names as required)
sudo groupadd cpugroup
sudo useradd -m -d /home/hpcstudent -s /bin/bash hpcstudent
sudo usermod -aG cpugroup hpcstudent
id hpcstudent
sudo passwd hpcstudent
""")

    # -------------------------
    # Questions
    # -------------------------
    with st.expander("❓ Questions — quick answers"):
        st.markdown(textwrap.dedent("""
        1. How do you list all users? -> `cut -d: -f1 /etc/passwd`
        2. How do you list all groups? -> `getent group` or `cut -d: -f1 /etc/group`
        3. How do you check your UID, GID, and groups? -> `id`
        4. How do you create a user with custom home? -> `sudo useradd -m -d /home/custom -s /bin/bash user`
        5. How do you append a user to a group? -> `sudo usermod -aG group user`
        6. How do you remove a user and home? -> `sudo userdel -r user` or `sudo deluser --remove-home user`
        7. How do you change a user’s password? -> `sudo passwd user`
        """))

    st.success("Linux Administration module updated — includes examples, practice tasks and safe interactive snippets. Run these on a test VM or container (do not test destructive commands on production!).")
