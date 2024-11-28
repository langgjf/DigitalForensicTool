# Define the path for the log file
$logFile = "C:\Users\langj\OneDrive\Documents\Y3\Y3T1\ICT3215DigitalForensics\Project\MonitorScripts\MonitorProcessLogfile.txt"  # Update this path
$alertHistory = @{}

# Set adjusted threshold values
$cpuThreshold = 70           # Normal CPU threshold for logging
$memoryThreshold = 700MB     # Normal memory threshold for logging
$cpuCriticalThreshold = 90   # Critical CPU threshold for alert
$memoryCriticalThreshold = 1500MB  # Critical memory threshold for alert

# Import the BurntToast module for notifications (make sure it's installed)
Import-Module BurntToast

while ($true) {
    $processes = Get-Process | Where-Object { 
        $_.CPU -gt $cpuThreshold -or $_.WorkingSet -gt $memoryThreshold 
    }

    foreach ($process in $processes) {
        $processName = $process.ProcessName
        $currentTime = Get-Date  # Keep $currentTime as a datetime object
        $cpuUsage = $process.CPU
        $memoryUsageMB = [math]::Round($process.WorkingSet / 1MB, 2)

        # Log and alert if above normal thresholds, with reduced frequency
        if ($alertHistory.ContainsKey($processName)) {
            if (($currentTime - $alertHistory[$processName]).TotalSeconds -gt 10) {
                $alertMessage = "[$($currentTime.ToString('yyyy-MM-dd HH:mm:ss'))] High usage detected: $processName, CPU: $cpuUsage%, Memory: $memoryUsageMB MB"
                Write-Output $alertMessage
                $alertMessage | Out-File -FilePath $logFile -Append
                $alertHistory[$processName] = $currentTime
            }
        } else {
            $alertMessage = "[$($currentTime.ToString('yyyy-MM-dd HH:mm:ss'))] High usage detected: $processName, CPU: $cpuUsage%, Memory: $memoryUsageMB MB"
            Write-Output $alertMessage
            $alertMessage | Out-File -FilePath $logFile -Append
            $alertHistory[$processName] = $currentTime
        }

        # Trigger notification only if above critical thresholds
        if ($cpuUsage -gt $cpuCriticalThreshold -or $memoryUsageMB -gt $memoryCriticalThreshold) {
            New-BurntToastNotification -Text "Critical Alert: $processName", "CPU: $cpuUsage%, Memory: $memoryUsageMB MB"
        }
    }

    Start-Sleep -Seconds 5 # Delay to avoid excessive CPU usage by the script itself
}

