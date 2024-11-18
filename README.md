# Background Task Analyzer Tool
## Install Dependencies:
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

## Open Source Procmon Set Up:
1) Download [openprocmon](https://github.com/progmboy/openprocmon). 
2) Extract the file into project directory. Eg. "C:\ICT3215\Project\openprocmon".
3) Open procmon_gui.vcxproj("C:\ICT3215\Project\openprocmon\gui").
4) Configure openprocmon to use the WTL installed by changing the 4 instances of "D:\source\WTL10_9163\Include" to "C:\ICT3215\Project\WTL10_10320_Release\Include".
5) Verify that the set up is successful by launching openprocmingui.exe("C:\ICT3215\Project\openprocmon\bin\Release\openprocmingui.exe") as an administrator.
![image](https://github.com/user-attachments/assets/50d2e8f2-d17b-4774-8ee6-9e712f52f869)

## Kiwi Syslog Server Set Up:
1) Download [Kiwi Syslog Server](https://www.solarwinds.com/free-tools/kiwi-free-syslog-server).
2) After installation, run the Kiwi Syslog Server Console as an administrator.
3) Navigate to Kiwi Syslog Server Setup -> Inputs -> UDP
4) Ensure that Listen for UDP Syslog messages is checked and UDP Port 514 is bind.
> [!IMPORTANT]  
> Ensure that Windows Firewall allows inbound and outbound traffic to port 514, else syslog message would not be captured.
5) Navigate to Kiwi Syslog Service Manager -> Manage -> Start the Syslogd service.
6) Kiwi Syslog Server is now ready to receive syslog messages.
