import subprocess
import re
import time
from datetime import datetime
import psutil
import socket

#Suspicious ports to monitor
SUSPICIOUS_PORTS = {6667, 12345, 31337, 4444, 5555, 69, 445, 1433, 8080, 3389}

#Syslog server config
SYSLOG_SERVER_IP = "127.0.0.1"
SYSLOG_SERVER_PORT = 514

#Netstat output, check for suspicious connections
def check_suspicious_ports():
    netstat_output = subprocess.check_output(['netstat', '-ano'], encoding='utf-8')

    #Save full netstat output to ref file with timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(f"netstat_output_{timestamp}.log", "w") as netstat_file:
        netstat_file.write(netstat_output)

    #Regex pattern to match netstat output
    pattern = re.compile(r'^\s*(TCP|UDP)\s+(\S+):(\d+)\s+(\S+):(\d+)\s+(\S+)\s*(\d+)$')

    print("Checking for suspicious connections...")

    for line in netstat_output.splitlines():
        match = pattern.match(line)
        if match:
            proto = match.group(1)
            local_address = match.group(2)
            local_port = int(match.group(3))
            foreign_address = match.group(4)
            foreign_port = int(match.group(5))
            state = match.group(6) if proto == "TCP" else "N/A"
            pid = match.group(7)

            #Check if local ports are in list of sus ports
            if local_port in SUSPICIOUS_PORTS:
                alert_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                #Get process name and path by PID
                try:
                    process = psutil.Process(int(pid))
                    process_name = process.name()
                    process_path = process.exe()  
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    process_name = "Unknown"
                    process_path = "Path not accessible"

                print(f"Suspicious connection detected at {alert_time}!")
                print(f"Protocol: {proto}")
                print(f"Local Address: {local_address}:{local_port}")
                print(f"Foreign Address: {foreign_address}:{foreign_port}")
                print(f"State: {state}")
                print(f"PID: {pid}")
                print(f"Process Name: {process_name}")
                print(f"Process Path: {process_path}")
                print("-" * 40)

                #Log details of sus connections with timestamp
                log_suspicious_connection(alert_time, proto, local_address, local_port, foreign_address, foreign_port, state, pid, process_name, process_path)
                #Send to syslog server
                send_to_syslog(alert_time, proto, local_address, local_port, foreign_address, foreign_port, state, pid, process_name, process_path)


def log_suspicious_connection(alert_time, proto, local_address, local_port, foreign_address, foreign_port, state, pid, process_name, process_path):
    """
    Logs sus connections to file with timestamp.
    """
    with open("suspicious_connections.log", "a") as log_file:
        log_file.write(f"Alert Time: {alert_time}\n")
        log_file.write(f"Suspicious connection detected!\n")
        log_file.write(f"Protocol: {proto}\n")
        log_file.write(f"Local Address: {local_address}:{local_port}\n")
        log_file.write(f"Foreign Address: {foreign_address}:{foreign_port}\n")
        log_file.write(f"State: {state}\n")
        log_file.write(f"PID: {pid}\n")
        log_file.write(f"Process Name: {process_name}\n")
        log_file.write(f"Process Path: {process_path}\n")
        log_file.write("-" * 40 + "\n")

def send_to_syslog(alert_time, proto, local_address, local_port, foreign_address, foreign_port, state, pid, process_name, process_path):
    """
    Send sus connection details to syslog.
    """
    message = (
        f"Suspicious connection detected! "
        f"Time: {alert_time}, Protocol: {proto}, Local Address: {local_address}:{local_port}, "
        f"Foreign Address: {foreign_address}:{foreign_port}, State: {state}, PID: {pid}, "
        f"Process: {process_name}, Path: {process_path}"
    )

    #Create UDP socket
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as syslog_socket:
        syslog_socket.sendto(message.encode('utf-8'), (SYSLOG_SERVER_IP, SYSLOG_SERVER_PORT))


if __name__ == "__main__":
    try:
        while True:
            check_suspicious_ports()
            time.sleep(60)
    except KeyboardInterrupt:
        print("Monitoring stopped.")
