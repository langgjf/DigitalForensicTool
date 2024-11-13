**ReadMe:**

In PowerShell (Admin):
-----------------------
1) Install the BurntToast module for notifications: 
- "Install-Module -Name BurntToast -Force -Scope CurrentUser"

On Windows:
------------
2) Copy the Script into a text editor on your VM.

3) Change the log path in the text editor. This is for saving logs: 
- $logFile = "C:\path\to\your\logfile.txt"  # Update this path

4) Save the script as "MonitorProcess.ps1" to your preferred path.

In Powershell (Admin):
----------------
5) Navigate to the folder where you saved "MonitorProcess.ps1"

6) Run the script: ".\MonitorProcess.ps1" 

Verify Script Functionality
---------------------------
1) Run your script & observe the output in the console.

2) Testing with Resource-Intensive Processes: 
- Open applications that consume high CPU or memory, like: 
	- Chrome with multiple tabs open
	- Streaming videos or gaming apps

3) Adjust Thresholds for Testing:
- Lower the thresholds temporarily (e.g., set CPU threshold to 10% or memory to 100MB) to trigger alerts more frequently, ensuring the script responds as expected.

Note:
-----
- Normal Alerts: Logs and displays high usage alerts every 10 seconds for each process if it exceeds the normal CPU and memory thresholds.

- Critical Pop-Up Alerts: Shows a Windows notification (using BurntToast) only if a process exceeds the higher cpuCriticalThreshold or memoryCriticalThreshold.

- Logging to File: Writes all alerts to a specified log file for record-keeping.




