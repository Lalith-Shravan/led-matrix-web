import os
import pwd
import sys

def drop_privileges(user="pi"):
    if os.getuid() != 0:
        return  # Already not running as root; nothing to do

    try:
        pw = pwd.getpwnam(user)
    except KeyError:
        print(f"[ERROR] User '{user}' not found. Perhaps you forgot to change the user in run.py?", file=sys.stderr)
        sys.exit(1)

    try:
        os.setgid(pw.pw_gid)
        os.setuid(pw.pw_uid)
        os.environ["HOME"] = pw.pw_dir
        print(f"[INFO] Dropped privileges to user '{user}' (UID: {pw.pw_uid}, GID: {pw.pw_gid})")
    except OSError as e:
        print(f"[ERROR] Failed to drop privileges: {e}", file=sys.stderr)
        sys.exit(1)