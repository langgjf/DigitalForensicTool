import subprocess
import threading
import os
import sys
import socket

# Syslog server config
SYSLOG_SERVER_IP = "127.0.0.1"
SYSLOG_SERVER_PORT = 514

# Get the directory where the current script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Function to send logs to syslog server
def send_to_syslog(message):
    """
    Send a log message to the syslog server.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as syslog_socket:
            syslog_socket.sendto(message.encode('utf-8'), (SYSLOG_SERVER_IP, SYSLOG_SERVER_PORT))
    except Exception as e:
        print(f"Error sending log to syslog: {e}")

# Function to start suspicious port monitoring
def start_suspicious_monitor():
    python_executable = sys.executable
    suspicious_monitor_path = os.path.join(script_dir, '../MonitorScripts', 'suspicious_port_monitor.py')
    subprocess.Popen([python_executable, suspicious_monitor_path])

# Function to execute PowerShell script for process monitoring
def execute_CPUusage_script():
    """
    Run the MonitorProcess.ps1 script and send logs to the syslog server.
    """
    monitor_process_path = os.path.join(script_dir, '../MonitorScripts', 'MonitorProcess.ps1')
    try:
        proc = subprocess.Popen(
            [
                "powershell.exe",
                "-ExecutionPolicy", "Bypass",
                "-File", monitor_process_path
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Automatically press "R" when prompted
        proc.stdin.write("R\n")
        proc.stdin.flush()

        # Send all to logs
        # Read and send logs to syslog
        # for line in iter(proc.stdout.readline, ''):
        #     log_message = line.strip()
        #     if log_message:  # Avoid empty lines
        #         print(f"Log: {log_message}")  
        #         send_to_syslog(log_message)

        # proc.stdin.close()
        # proc.wait()  # Wait for the process to finish
        # END

        # Send 5 lines
        # Counter for the number of logs sent
        log_count = 0
        max_logs = 5  # Maximum number of logs to send

        # Read logs and send only the first 5 entries to the syslog server
        for line in iter(proc.stdout.readline, ''):
            log_message = line.strip()
            if log_message:  # Avoid empty lines
                print(f"Log: {log_message}")  
                send_to_syslog(log_message)
                log_count += 1

                # Stop after sending the specified number of logs
                if log_count >= max_logs:
                    print(f"Sent {max_logs} logs. Stopping monitoring.")
                    break

        # Terminate the PowerShell process
        proc.terminate()
        proc.wait()  # Ensure the process has completely stopped
        # Send 5 to logs END

    except Exception as e:
        print(f"Failed to execute PowerShell script for CPU Monitor: {e}")

# Function to execute PowerShell script for admin privilege check
def execute_AdminPriv_script():
    check_script_path = os.path.join(script_dir, '../MonitorScripts', 'CheckProcessElevation.ps1')
    try:
        proc = subprocess.Popen(
            [
                "powershell.exe",
                "-ExecutionPolicy", "Bypass",
                "-File", check_script_path
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        #Send all logs to syslog
        # for line in iter(proc.stdout.readline, ''):  
        #     log_message = line.strip()
        #     #print(log_message)  
        #     send_to_syslog(log_message)
        # END

        # Send 5 lines
        line_count = 0  
        for line in iter(proc.stdout.readline, ''):
            log_message = line.strip()
            print(log_message)
            send_to_syslog(log_message)
            
            line_count += 1  # Increment the counter
            if line_count >= 5:  # Check if the limit is reached
                break
        # Ensure the process is terminated if the loop is exited early
        proc.terminate()
        proc.wait()
        # Send 5 to logs END
        
    except subprocess.CalledProcessError as e:
        print(f"Failed to execute PowerShell script for Admin Privilege: {e}")

# Function to monitor IP Addr
def execute_IPadd_script():
    ip_add_script_path = os.path.join(script_dir, '../MonitorScripts', 'IPaddProcess.ps1')
    try:
        proc = subprocess.Popen(
            [
                "powershell.exe",
                "-ExecutionPolicy", "Bypass",
                "-File", ip_add_script_path
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        #Send all logs to syslog
        # for line in iter(proc.stdout.readline, ''):  
        #     log_message = line.strip()
        #     #print(log_message)  
        #     send_to_syslog(log_message)
        # END

        # Send 5 lines
        line_count = 0  
        for line in iter(proc.stdout.readline, ''):
            log_message = line.strip()
            print(log_message)
            send_to_syslog(log_message)
            
            line_count += 1  
            if line_count >= 5:  
                break
        # Ensure the process is terminated if the loop is exited early
        proc.terminate()
        proc.wait()
        # Send 5 to logs END

    except subprocess.CalledProcessError as e:
        print(f"Failed to execute PowerShell script for IP Address Monitoring: {e}")

# Start openprocmingui.exe
openprocmon_exe_path = os.path.join(script_dir, '../openprocmon-master', 'bin', 'Release', 'openprocmingui.exe')
subprocess.Popen([openprocmon_exe_path])
    
# Start monitoring threads
monitor_thread = threading.Thread(target=start_suspicious_monitor)
monitor_thread.start()

# Execute PowerShell script for MonitorProcess.ps1
monitor_process_thread = threading.Thread(target=execute_CPUusage_script)
monitor_process_thread.start()

# Execute PowerShell script for CheckProcessElevation.ps1
admin_priv_thread = threading.Thread(target=execute_AdminPriv_script)
admin_priv_thread.start()

# Execute PowerShell script for IPaddProcess.ps1
ip_add_thread = threading.Thread(target=execute_IPadd_script)
ip_add_thread.start()