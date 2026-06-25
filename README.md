FlashDrop
Wirelessly send and receive files to/from a USB flash drive using your phone, no internet,
no app, no cables needed.
How it works
1. Plug in your flash drive
2. Your PC automatically creates a WiFi hotspot
3. A QR code window pops up on your screen
4. Connect your phone to the hotspot and scan the QR code
5. Your phone browser opens a page where you can upload files to the drive or download
files from it
Built with
Python 3 (standard library only)
qrencode for QR code generation
nmcli for hotspot management
udev rules for auto-trigger on plug-in
tkinter for the QR code display window
Requirements
Linux PC (tested on Ubuntu 22.04)
Python 3
qrencode
python3-tkBefore You Start — Gather Your Info
Before editing any files, run these commands to collect the values you will need:
Your Linux username:
whoami
This will print your username e.g. john . Every time you see YOUR_USERNAME in this guide,
replace it with this.
Your flash drive mount path:
lsblk
Look for your drive. It will be mounted at something like /media/YOUR_USERNAME/DRIVENAME .
To confirm:
ls /media/YOUR_USERNAME/DRIVENAME
If your files appear, that is the correct path. Every time you see YOUR_DRIVE_PATH in this
guide, replace it with this full path.
Your WiFi interface name:
ip link
Look for a name starting with w such as wlan0 , wlp1s0 , or wlp2s0 . Every time you see
YOUR_WIFI_INTERFACE in this guide, replace it with this.
Your flash drive UUID:
lsblk -o NAME,UUID,LABEL
Find your drive and copy its UUID e.g. A7C8-0792 . Every time you see YOUR_DRIVE_UUID in
this guide, replace it with this.
Your hotspot IP address:
First create the hotspot temporarily:
nmcli device wifi hotspot ifname YOUR_WIFI_INTERFACE ssid "FileDrop" password "12345678"Then check the IP:
ip addr show YOUR_WIFI_INTERFACE
Look for the line starting with inet . The IP is usually 10.42.0.1 . Every time you see
YOUR_HOTSPOT_IP in this guide, replace it with this.
Then turn off the hotspot for now:
nmcli connection down Hotspot
Setup
1. Install dependencies
sudo apt install qrencode python3-tk -y
2. Edit fileserver.py
Open the file:
nano ~/fileserver.py
At the very top find this line:
SAVE_DIR = "/media/joe/A7C8-0792"
Change it to your flash drive path:
SAVE_DIR = "YOUR_DRIVE_PATH"
Example:
SAVE_DIR = "/media/john/USB-DRIVE"
Save with Ctrl+O then Enter then Ctrl+X.3. Edit flashdrop.sh
Open the file:
nano ~/flashdrop.sh
Find and update every line that contains a path or value specific to the original setup:
Line with hotspot creation — replace the interface name:
nmcli device wifi hotspot ifname YOUR_WIFI_INTERFACE ssid "FileDrop" password "12345678"
Line that kills the server — replace the username:
pkill -f fileserver.py
python3 /home/YOUR_USERNAME/fileserver.py &
Line that removes old QR image — replace the username:
sudo rm -f /home/YOUR_USERNAME/qr.png
Line that generates the QR code — replace the username and IP:
qrencode -o /home/YOUR_USERNAME/qr.png "http://YOUR_HOTSPOT_IP:8080"
Line that creates the trigger file — replace the username:
touch /home/YOUR_USERNAME/show_qr_trigger
Log file line at the top — replace the username:
exec > /home/YOUR_USERNAME/flashdrop.log 2>&1
Save with Ctrl+O then Enter then Ctrl+X.
4. Edit qrwatcher.sh
Open the file:
nano ~/qrwatcher.shFind and update every line that contains a path:
Line that starts the server — replace the username:
nohup python3 /home/YOUR_USERNAME/fileserver.py > /home/YOUR_USERNAME/server.log 2>&1 &
Line that checks for the trigger file — replace the username:
if [ -f /home/YOUR_USERNAME/show_qr_trigger ]; then
Line that removes the trigger file — replace the username:
rm /home/YOUR_USERNAME/show_qr_trigger
Line that runs the QR display — replace the username:
python3 /home/YOUR_USERNAME/showqr.py
Save with Ctrl+O then Enter then Ctrl+X.
5. Edit showqr.py
Open the file:
nano ~/showqr.py
Find this line and replace the username and IP:
subprocess.run(["qrencode", "-o", "/home/YOUR_USERNAME/qr.png", "-s", "10", "http://YOUR_HOTS
Find this line and replace the username:
img = tk.PhotoImage(file="/home/YOUR_USERNAME/qr.png")
Save with Ctrl+O then Enter then Ctrl+X.
6. Make the scripts executable
chmod +x ~/flashdrop.sh ~/qrwatcher.sh7. Create the udev rule
This triggers everything automatically when you plug in your flash drive.
sudo nano /etc/udev/rules.d/99-flashdrop.rules
Paste this single line, replacing the values with yours:
ACTION=="add", ENV{ID_FS_UUID}=="YOUR_DRIVE_UUID", RUN+="/home/YOUR_USERNAME/flashdrop.sh"
Example:
ACTION=="add", ENV{ID_FS_UUID}=="A7C8-0792", RUN+="/home/john/flashdrop.sh"
Save and reload:
sudo udevadm control --reload-rules
8. Set up autostart
This makes the watcher start automatically every time you log in.
mkdir -p ~/.config/autostart
nano ~/.config/autostart/qrwatcher.desktop
Paste this, replacing YOUR_USERNAME with your Linux username:
[Desktop Entry]
Type=Application
Name=QR Watcher
Exec=bash /home/YOUR_USERNAME/qrwatcher.sh
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Save with Ctrl+O then Enter then Ctrl+X.9. Reboot
sudo reboot
After rebooting, plug in your flash drive and everything starts automatically.
Usage
Send to Drive — tap the file picker on the web page, select one or multiple files, tap
Send to Flash Drive
Get from Drive — switch to the Get from Drive tab, browse all files on the flash drive,
tap Download next to any file to save it to your phone
Notes
Works on any phone browser — Chrome, Firefox, Safari
Default hotspot name: FileDrop
Default hotspot password: 12345678
You can change both in flashdrop.sh
The web page runs on port 8080
Files are saved to the root of the flash drive
Author
Built by Joe — @EligibleFreak
