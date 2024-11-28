# Define Windows API functions
Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;

public class Advapi32 {
    [DllImport("advapi32.dll", SetLastError = true)]
    public static extern bool OpenProcessToken(IntPtr ProcessHandle, uint DesiredAccess, ref IntPtr TokenHandle);

    [DllImport("advapi32.dll", SetLastError = true)]
    public static extern bool GetTokenInformation(IntPtr TokenHandle, int TokenInformationClass, byte[] TokenInformation, int TokenInformationLength, ref int ReturnLength);

    [DllImport("kernel32.dll", SetLastError = true)]
    public static extern bool CloseHandle(IntPtr hObject);
}
"@

# Define constants for token access and token information
$TOKEN_QUERY = 0x0008
$TokenElevation = 20

# Get the list of running processes
$processes = Get-Process

# Iterate through each process
foreach ($process in $processes) {
    try {
        # Get process handle using .NET
        $processHandle = [System.Diagnostics.Process]::GetProcessById($process.Id).Handle
        $tokenHandle = New-Object IntPtr
        $elevated = $false

        # Open process token
        $null = [Advapi32]::OpenProcessToken($processHandle, $TOKEN_QUERY, [ref]$tokenHandle)

        if ($tokenHandle -ne [IntPtr]::Zero) {
            # Prepare buffer for token elevation information
            $elevation = New-Object byte[] 4
            $returnLength = [ref]0

            # Retrieve token elevation information
            $null = [Advapi32]::GetTokenInformation($tokenHandle, $TokenElevation, $elevation, $elevation.Length, $returnLength)

            # Check if elevation flag is set
            $isElevated = [BitConverter]::ToInt32($elevation, 0) -ne 0
            $elevated = $isElevated

            # Close the token handle
            $null = [Advapi32]::CloseHandle($tokenHandle)
        }

        # Determine and display the elevation status
        $elevationStatus = if ($elevated) { "Elevated" } else { "Not Elevated" }
        Write-Output "Process: $($process.Name) | ID: $($process.Id) | Elevation Status: $elevationStatus"
    } catch {
        # Handle errors (e.g., access denied)
        Write-Output "Process: $($process.Name) | ID: $($process.Id) | Error: Unable to retrieve elevation status"
    }
}
