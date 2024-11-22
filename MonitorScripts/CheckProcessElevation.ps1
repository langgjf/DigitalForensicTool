# Get the list of running processes
$processes = Get-Process

# Iterate through each process
foreach ($process in $processes) {
    try {
        # Query the Win32_Process WMI class for the specific process using its ProcessId
        $query = "SELECT * FROM Win32_Process WHERE ProcessId = $($process.Id)"
        $wmiProcess = Get-WmiObject -Query $query

        foreach ($item in $wmiProcess) {
            # Use WindowsPrincipal and WindowsIdentity to check if the process is elevated
            $elevated = (New-Object System.Security.Principal.WindowsPrincipal(
                            [System.Security.Principal.WindowsIdentity]::GetCurrent()
                         )).IsInRole([System.Security.Principal.WindowsBuiltInRole]::Administrator)
            
            # Determine the elevation status: Elevated or Not Elevated
            $elevationStatus = if ($elevated) { "Elevated" } else { "Not Elevated" }

            # Output the process details
            Write-Output "Process: $($process.Name) | ID: $($process.Id) | Elevation Status: $elevationStatus"
        }
    } catch {
        # Handle errors (e.g., if the script doesn't have access to certain processes)
        Write-Output "Process: $($process.Name) | ID: $($process.Id) | Error: Unable to retrieve elevation status"
    }
}
