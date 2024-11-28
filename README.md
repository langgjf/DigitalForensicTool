# SmartProc (Background Task Analyzer Tool)
SmartProc is a background task analyzer tool integrated with Procmon. 

SmartProc is capable of the following features:
1) Monitor and alert of suspicious port connections
2) Monitor and alert of suspicious IP addresses
3) Monitor and alert for processes running with administrator privileges
4) Monitor and alert for resource-intensive processes

# Table of contents
1. [Set Up](#setup)
    1. [Install Dependencies](#dependencies)
    2. [Open Source Procmon Set Up](#procmon)
    3. [Kiwi Syslog Server Set Up](#syslog)
2. [Usage Instructions](#usage)
    1. [Port Connection Monitoring](#port)
    2. [IP Address Monitoring](#IP)
    3. [Administrative Privileges Monitoring](#admin)
    4. [Resource Usage Monitoring](#resource)

# Set Up <a name="setup"></a>
## Install Dependencies: <a name="dependencies"></a>
1) Install Step 1, 2 and 3 from [Windows Driver Kit(WDK)](https://learn.microsoft.com/en-us/windows-hardware/drivers/download-the-wdk) for developing, testing and deploying drivers for Windows operating systems.
2) Install [Windows Template Library(WTL)](https://sourceforge.net/projects/wtl/) used for developing Windows applications and UI components.
3) Place WTL in project folder. Eg. "C:\ICT3215\Project\WTL10_10320_Release"
4) Install [Cmake](https://github.com/Kitware/CMake/releases/download/v3.31.0/cmake-3.31.0-windows-x86_64.msi) to build and compile OpenProcmon.
5) Open up an administrative command prompt in the project directory.
6) Run Cmake to configure building with Visual Studio 2022 setting the path to WTL and WDK.
```
cmake -G "Visual Studio 16 2022" -A X64 -DWTL_ROOT_DIR=C:\ICT3215\Project\WTL10_10320_Release -DWDK_WINVER=0x0A00
```
> [!NOTE]  
> Where IDE is Visual Studio 2022 with version 16.
7) Build the project.
```
cmake --build . --config Release
```
8) Enable test signing on Windows.
```
bcdedit /set testsigning on
``` 
9) Create a self-signed certificate in project directory.
```
Makecert -r -pe -ss PrivateCertStore -n "CN=MyCert" MyCert.cer
```
10) Use the certificate generated to digitally sign the openprocmon driver file so that Windows deem the driver file to be trustworthy for installation and execution. 
```
signtool sign /v /s PrivateCertStore /n MyCert /fd SHA256 /tr http://timestamp.digicert.com/ /td SHA256 C:\ICT3215\Project\openprocmon\bin\Release\procmon.sys
```    

## Open Source Procmon Set Up: <a name="procmon"></a>
1) Download [openprocmon](https://github.com/progmboy/openprocmon). 
2) Extract the file into project directory. Eg. "C:\ICT3215\Project\openprocmon".
3) Open procmon_gui.vcxproj("C:\ICT3215\Project\openprocmon\gui").
4) Configure openprocmon to use the WTL installed by changing the 4 instances of "D:\source\WTL10_9163\Include" to "C:\ICT3215\Project\WTL10_10320_Release\Include".
5) Verify that the set up is successful by launching openprocmingui.exe("C:\ICT3215\Project\openprocmon\bin\Release\openprocmingui.exe") as an administrator.
![image](https://github.com/user-attachments/assets/50d2e8f2-d17b-4774-8ee6-9e712f52f869)

## Kiwi Syslog Server Set Up: <a name="syslog"></a>
1) Download [Kiwi Syslog Server](https://www.solarwinds.com/free-tools/kiwi-free-syslog-server).
2) After installation, run the Kiwi Syslog Server Console as an administrator.
3) Navigate to Kiwi Syslog Server Setup -> Inputs -> UDP
4) Ensure that Listen for UDP Syslog messages is checked and UDP Port 514 is bind.
> [!IMPORTANT]  
> Ensure that Windows Firewall allows inbound and outbound traffic to port 514, else syslog message would not be captured.
5) Navigate to Kiwi Syslog Service Manager -> Manage -> Start the Syslogd service.
6) Kiwi Syslog Server is now ready to receive syslog messages.
# Usage Instructions <a name="usage"></a>
1) Clone the repository and unzip in project directory. Eg. "C:\ICT3215\Project\SmartProc"
2) Navigate to RunTimeExecution folder. "C:\ICT3215\Project\SmartProc\RunTimeExecution"
3) Open an administrative PowerShell in the RunTimeExecution directory.
4) Execute SmartProc via the following command.
```
python startSmartProc.py
```
5) Congratulations! SmartProc is now monitoring background processes, port connections, IP addresses, processes with administrative privileges and resource usage.
6) Any violations or suspicious activities will now be flagged and sent to the Kiwi Syslog server for further analysis.
## Port Connection Monitoring: <a name="port"></a>
1) SmartProc has been configured to monitor for suspicious port connections every 60 seconds.
The following table shows the ports and their corresponding vulnerability that SmartProc monitors for.

| Port | Usage | Vulnerability |
| --- | --- | --- |
| 69 | Trivial File Transfer Protocol for transferring configuration files   | Exploit for unauthorized file transfers |
| 445 | File and printer sharing | Exploit for ransomware and lateral movement |
| 1433 | Database connections | Exploit SQL injection and privilege escalation |
| 3389 | Remote Desktop Protocol for remote administration | Exploit for ransomware and lateral movement |
| 4444 | For remote shells | Exploit by worms and malware for backdoor |
| 5555 | Android Debug Bridge used by IoT devices | Utilized by unauthorized remote administration tools |
| 6667 | For chat applications and Internet Relay Chat services | Exploit by malware for command-and-control communications |
| 8080 | HTTP proxy | Exploit for SQL injection and directory traversal |
| 12345 | Remote administration tool | Remote access trojan exploitation to control infected machines |
| 31337 | - | Remote access trojan exploitation to control infected machines |

2) For simulation of suspicious port connection, open an administrative PowerShell.
```
# Example for opening a TCP listener on port 6667, indicative of malware C2
$listener = [System.Net.Sockets.TcpListener]6667
$listener.Start()
```
> [!IMPORTANT]  
> To close the open connection on port 6667, simply close the administrative PowerShell session.
3) SmartProc should capture the suspicious port connections, flag the connections and send the suspicious connections to the Kiwi Syslog server.
4) The Kiwi Syslog server should successfully receive the suspicious logs.
![image](https://github.com/user-attachments/assets/f59d6f25-2357-47dd-9a5a-0ad1158341ab)
5) The captured details of time, IP address, PID, process name and path relating to the suspicious port connections would greatly help forensic investigators in identifying the extent of compromise.

## IP Address Monitoring: <a name="IP"></a>
1) SmartProc has been configured to monitor for suspicious IP addresses.
> [!IMPORTANT]  
> Change the path of the log file in IPaddProcess.ps1 to save the logs as a text file in the local machine
```
$logFile = "C:\path\to\your\IPProcesslogfile.txt"
```
2) SmartProc should capture the suspicious IP addresses, save the information in a log file and send them to the Kiwi Syslog server.
3) The Kiwi Syslog server should successfully receive the suspicious logs.
![image](https://github.com/user-attachments/assets/16d5adb0-6cd8-4d60-b1bc-57328fe0fdc9)
![image](https://github.com/user-attachments/assets/c05b4736-94d8-48fd-837d-fcaab03ff50e)

4) The captured details of timestamp, Protocol, Local IP address, Remote IP address, PID, Process Name and Process Start Time relating to the suspicious IP addresses would greatly help forensic investigators in identifying the extent of compromise.

## Administrative Privileges Monitoring: <a name="admin"></a>
1) SmartProc has been configured to also capture and display for processes that uses elevated administrative privileges.
> [!IMPORTANT]  
> Run the following command. This command allows the script to run for the current PowerShell session only.
```
Set-ExecutionPolicy RemoteSigned -Scope Process  
```
2) SmartProc will start to query the Win32_Process WMI class for the specific process using its ProcessId. it will then use the WindowsPrincipal and WindowsIdentity to check if the process is elevated.
3) The Kiwi server will then receive logs relating to the elevation status of the processes running.
![image](https://github.com/user-attachments/assets/6885352f-d4c8-46c8-893e-abd8b7d228b2)

4) It will show the process name, its ID and elevation status.


## Resource Usage Monitoring: <a name="resource"></a>
#### In PowerShell (Admin):
1) Install the `BurntToast` module for alert notifications:
     ```powershell
     Install-Module -Name BurntToast -Force -Scope CurrentUser
     ```
#### On Windows:
2) Copy the provided script using Text Editor in your project directory.
3) Update the log file path in the script:
     ```powershell
     $logFile = "C:\path\to\your\logfile.txt"
     ```
4) Save the provided script as `MonitorProcess.ps1` in your project directory.
#### In PowerShell (Admin):
5) Open PowerShell with Administrator privileges.
6) Navigate to the directory containing `MonitorProcess.ps1`.
7) Execute the script:
     ```powershell
     .\MonitorProcess.ps1
     ```

---
### Usage Instructions
1. **Testing Resource Monitoring**:
   - Open resource-heavy applications like Chrome with multiple tabs, video streaming apps, or gaming software.
   - Observe the alerts generated in the PowerShell console or via Windows notifications.

2. **Adjusting Thresholds**:
   - Update the script’s thresholds for testing:
     - CPU Threshold: Adjust `cpuThreshold` to trigger alerts for specific usage levels.
     - Memory Threshold: Adjust `memoryThreshold` to monitor processes consuming specified amounts of memory.

3. **Log Analysis**:
   - Analyze logs stored at the specified path (e.g., `C:\path\to\your\logfile.txt`).
   - Logs can be reviewed locally or on the Kiwi Syslog Server.

---
