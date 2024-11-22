# Define the path for the log file
$logFile = "C:\Users\langj\OneDrive\Documents\Y3\Y3T1\ICT3215DigitalForensics\Project\MonitorScripts\MonitorProcessLogfile.txt"  # Update this path
$alertHistory = @{}

# Set threshold values
$cpuThreshold = 80           # Normal threshold for logging
$memoryThreshold = 500MB     # Normal threshold for logging
$cpuCriticalThreshold = 500   # Higher threshold for critical alert
$memoryCriticalThreshold = 300MB  # Higher threshold for critical alert

# Import the BurntToast module for notifications (make sure it's installed)
Import-Module BurntToast

while ($true) {
    $processes = Get-Process | Where-Object { 
        $_.CPU -gt $cpuThreshold -or $_.WorkingSet -gt $memoryThreshold 
    }

    foreach ($process in $processes) {
        $processName = $process.ProcessName
        $currentTime = Get-Date
        $cpuUsage = $process.CPU
        $memoryUsageMB = [math]::Round($process.WorkingSet / 1MB, 2)

        # Log and alert if above normal thresholds, with reduced frequency
        if ($alertHistory.ContainsKey($processName)) {
            if (($currentTime - $alertHistory[$processName]).TotalSeconds -gt 10) {
                $alertMessage = "High usage detected: $processName, CPU: $cpuUsage, Memory: $memoryUsageMB MB"
                Write-Output $alertMessage
                $alertMessage | Out-File -FilePath $logFile -Append
                $alertHistory[$processName] = $currentTime
            }
        } else {
            $alertMessage = "High usage detected: $processName, CPU: $cpuUsage, Memory: $memoryUsageMB MB"
            Write-Output $alertMessage
            $alertMessage | Out-File -FilePath $logFile -Append
            $alertHistory[$processName] = $currentTime
        }

        # Trigger notification only if above critical thresholds
        if ($cpuUsage -gt $cpuCriticalThreshold -or $memoryUsageMB -gt $memoryCriticalThreshold) {
            New-BurntToastNotification -Text "Critical Alert: $processName", "CPU: $cpuUsage, Memory: $memoryUsageMB MB"
        }
    }

    Start-Sleep -Seconds 5 # Delay to avoid excessive CPU usage by the script itself
}
