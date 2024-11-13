# Run netstat and skip the first few lines (header lines)
$netstatOutput = netstat -ano

foreach ($line in $netstatOutput) {
    # Split line by whitespace (this splits by any number of spaces or tabs)
    $parts = $line -split "\s+"
    
    # Handle cases where there are enough parts (at least 4)
    if ($parts.Length -ge 4) {
        # Assign fields based on number of columns
        $protocol = $parts[1]
        $localAddress = $parts[2]
        $remoteAddress = $parts[3]
        
        # If the protocol is TCP, it will have a "State" field
        if ($protocol -eq "TCP" -and $parts.Length -ge 5) {
            $state = $parts[4]
            $processID = $parts[5]
        }
        # If the protocol is UDP, there is no state
        elseif ($protocol -eq "UDP" -and $parts.Length -ge 4) {
            $state = "N/A"
            $processID = $parts[4]
        }
        else {
            continue
        }

        # Get the process name by PID
        try {
            $process = Get-Process -Id $processID -ErrorAction Stop
            $processName = $process.ProcessName
        }
        catch {
            $processName = "Unknown"
        }

        # Display connection details
        Write-Output "Protocol: $protocol, Local Address: $localAddress, Remote Address: $remoteAddress, State: $state, Process ID: $processID, Process Name: $processName"
    }
}
