import psutil
import re
import os
import subprocess
import time

# Hardcoded paths
OPENPROCMON_EXE_PATH = r"C:\Users\user\Desktop\DigitalForensics\DFProj\openprocmon-master\openprocmon-master\bin\Release\openprocmingui.exe"
PATTERNS_FILE_PATH = r"C:\Users\user\Desktop\DigitalForensics\DFProj\MaliciousFilter\suspicious_patterns.txt"


def load_suspicious_patterns(file_path):
    """Load suspicious patterns from a text file."""
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return [line.strip() for line in f if line.strip()]
    else:
        print(f"Error: Patterns file not found at {file_path}")
        return []


def start_openprocmon():
    """Start the openprocmon GUI executable."""
    if os.path.exists(OPENPROCMON_EXE_PATH):
        print("Starting openprocmon...")
        subprocess.Popen([OPENPROCMON_EXE_PATH], shell=True)  # Open in a new process
    else:
        print(f"Error: openprocmon executable not found at {OPENPROCMON_EXE_PATH}")


def check_processes(suspicious_patterns):
    """Check processes for suspicious names and log results."""
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            process_name = proc.info['name']
            process_id = proc.info['pid']

            # Check against suspicious patterns
            if any(re.search(pattern, process_name, re.IGNORECASE) for pattern in suspicious_patterns):
                message = f"Suspicious process detected: {process_name} (PID: {process_id})"
                print(message)  # Print to CMD
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue


def run_openprocmon_and_monitor():
    """Launch OpenProcMon and monitor processes every 5 seconds."""
    # Start OpenProcMon
    start_openprocmon()

    # Load suspicious patterns from the hardcoded file path
    suspicious_patterns = load_suspicious_patterns(PATTERNS_FILE_PATH)
    if not suspicious_patterns:
        print("No suspicious patterns loaded. Exiting.")
        exit(1)

    print("Monitoring processes for suspicious names every 5 seconds...")

    # Continuous monitoring every 5 seconds
    while True:
        print("Checking processes...")
        check_processes(suspicious_patterns)
        time.sleep(5)  # Wait for 5 seconds before checking again


if __name__ == "__main__":
    # Run OpenProcMon and start monitoring
    run_openprocmon_and_monitor()
