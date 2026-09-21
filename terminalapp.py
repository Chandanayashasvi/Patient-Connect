import os
import subprocess
import sys

def run_command(command):
    print(f"\n> {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)
    return result.returncode

if __name__ == "__main__":
    project_dir = r"C:\Users\chand\PatientConnect"
    os.chdir(project_dir)

    commands = [
        "py .\\db.py",
        "py .\\seed.py",
        "py .\\patientconnect_cli.py",
    ]

    for cmd in commands:
        code = run_command(cmd)
        if code != 0:
            print(f"Command failed with exit code {code}: {cmd}")
            break