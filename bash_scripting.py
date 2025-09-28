# bash_scripting.py
import streamlit as st
import textwrap

def _code(cmd: str):
    """Helper to show bash code blocks with cleaned indentation."""
    st.code(textwrap.dedent(cmd).strip(), language="bash")

def render():
    st.header("📜 Bash Scripting Mastery")
    st.markdown("""
    Goal: Become fluent at automating admin tasks using Bash.  
    Use scripts to handle users, logs, loops, conditionals, and scheduled jobs.
    """)

    # -------------------------
    # Variables & Arguments
    # -------------------------
    with st.expander("🔑 Variables & Arguments"):
        st.markdown("**Basics of Bash variables and script arguments:**")
        _code("""#!/bin/bash
# Define a variable
NAME="HPCStudent"
echo "Hello $NAME"

# Special variables
$0   # script name
$1   # first argument
$@   # all arguments
$#   # number of arguments
$(command)  # command substitution
""")

        st.subheader("Practice: Script to create a user from argument")
        _code("""#!/bin/bash
if [ $# -eq 0 ]; then
    echo "Usage: $0 <username>"
    exit 1
fi

USER=$1
sudo useradd -m -s /bin/bash "$USER"
echo "User $USER created"
""")

        st.markdown("**Interactive generator:**")
        uname = st.text_input("Enter username", value="hpcuser", key="bash_var_user")
        if st.button("Show script for single user creation"):
            script = f"""#!/bin/bash
USER={uname}
sudo useradd -m -s /bin/bash "$USER"
echo "User $USER created"
"""
            _code(script)

    # -------------------------
    # Loops & Conditionals
    # -------------------------
    with st.expander("🔄 Loops & Conditionals"):
        st.markdown("**Loop and conditional constructs in Bash.**")
        _code("""# if-else example
if [ -f /etc/passwd ]; then
    echo "passwd file exists"
else
    echo "passwd file missing"
fi

# for loop
for i in 1 2 3; do
    echo "Number $i"
done

# while loop
count=1
while [ $count -le 3 ]; do
    echo "Count $count"
    count=$((count+1))
done
""")

        st.subheader("Practice: Loop through usernames from a CSV and create accounts")
        _code("""#!/bin/bash
INPUT="users.csv"
while IFS=, read -r username; do
    sudo useradd -m -s /bin/bash "$username"
    echo "Created $username"
done < "$INPUT"
""")

    # -------------------------
    # File & Log Operations
    # -------------------------
    with st.expander("📂 File & Log Operations"):
        st.markdown("**Redirection, pipes, and text-processing tools.**")
        _code("""# Redirect
echo "hello" > file.txt     # overwrite
echo "world" >> file.txt    # append

# Pipe
cat /etc/passwd | grep root

# cut
cut -d: -f1 /etc/passwd

# awk
awk -F: '{print $1,$3}' /etc/passwd

# sed (replace)
sed 's/root/admin/' file.txt
""")

        st.subheader("Practice: Parse a log file and extract error messages")
        _code("""#!/bin/bash
LOGFILE="/var/log/syslog"
grep -i "error" "$LOGFILE" > errors.txt
echo "Errors extracted to errors.txt"
""")

    # -------------------------
    # Automation & Cron
    # -------------------------
    with st.expander("⏰ Automation & Cron"):
        st.markdown("**Schedule scripts with cron.**")
        _code("""# Edit crontab
crontab -e

# Run every 10 minutes
*/10 * * * * /home/user/health_check.sh
""")

        st.subheader("Practice: System health logger")
        _code("""#!/bin/bash
OUT="/tmp/sys_health.log"
echo "=== $(date) ===" >> $OUT
uptime >> $OUT
free -h >> $OUT
df -h >> $OUT
echo "Logged system health to $OUT"
""")

        st.markdown("Then add to cron:")
        _code("*/10 * * * * /home/user/health_check.sh")

    # -------------------------
    # Exercises
    # -------------------------
    with st.expander("📝 Exercises"):
        st.markdown("""
        1. Write a script that accepts 2 numbers as arguments and prints their sum.  
        2. Write a for loop that pings a list of hosts and logs which are reachable.  
        3. Write a while loop that monitors `/tmp/testfile` and echoes when it changes.  
        4. Write a script to rotate a log file (`mv logfile logfile.old`).  
        5. Write a cron job that clears `/tmp` every midnight.  
        """)

    # -------------------------
    # Interview Drill
    # -------------------------
    with st.expander("❓ Interview Drill — quick Q&A"):
        st.markdown(textwrap.dedent("""
        1. `$0` vs `$@` vs `$#`?  
        - `$0` script name, `$@` all args, `$#` number of args.  

        2. Difference between `>` and `>>`?  
        - `>` overwrite, `>>` append.  

        3. How to run a script every 10 min?  
        - `*/10 * * * * script.sh` in crontab.  

        4. How to replace all occurrences of "foo" with "bar" in file?  
        - `sed -i 's/foo/bar/g' file`.  

        5. How to extract only usernames from `/etc/passwd`?  
        - `cut -d: -f1 /etc/passwd`.  
        """))

    st.success("Bash Scripting module loaded — learn, practice and drill interactively.")
