**ReadMe:**

In PowerShell (Admin):
-----------------------
1) Enable Powershell to run script: 
- Type Set-ExecutionPolicy Unrestricted.
- Press Enter.
- Type A.

On Windows:
------------
2) Copy the Script into a text editor on your VM.

3) Change the log path in the text editor. This is for saving logs: 
- $logFile = "C:\path\to\your\IPProcesslogfile.txt"  # Update this path

4) Save the script as "IPaddProcess.ps1" to your preferred path.

In Powershell (Admin):
----------------
5) Navigate to the folder where you saved "IPaddProcess.ps1"

6) Run the script: ".\IPaddProcess.ps1" 

Verify Script Functionality
---------------------------
1) Run your script & observe the output in the console.

2) Testing with Resource-Intensive Processes: 
- Open applications that consume high CPU or memory, like: 
	- Chrome, Microsoft Edge with multiple tabs open
        - Watching videos and music via Youtube

Note:
-----
- Disable Powershell Script: Type Set-ExecutionPolicy Restricted in PowerShell (admin)
- Idle process: A system process that doesn’t have a conventional start time as it is essentially always present when the system is running
- Logging to File: Writes all alerts to a specified log file for record-keeping.
