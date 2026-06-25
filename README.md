FlashDrop
Wirelessly send and receive files to/from a USB flash drive using your phone — no internet,
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
python3-tkSetup
1. Install dependencies
sudo apt install qrencode python3-tk -y
2. Find your flash drive mount path
Plug in your flash drive, then run:
lsblk
Look for your drive under the NAME column. It will usually be mounted at a path like:
/media/yourname/DRIVENAME
For example: /media/joe/A7C8-0792
To confirm, run:
ls /media/yourname/DRIVENAME
If it lists your files, that is the correct path.
3. Find your WiFi interface name
Run:
ip link
Look for a name starting with w such as wlan0 , wlp1s0 , or wlp2s0 . That is your WiFi
interface name.
4. Find your flash drive UUID
Run:lsblk -o NAME,UUID,LABEL
Look for your drive and copy the UUID value. It looks something like A7C8-0792 .
5. Find your hotspot IP address
After creating the hotspot (Step 8), run:
ip addr show YOUR_WIFI_INTERFACE
Replace YOUR_WIFI_INTERFACE with the name from Step 3. Look for the line starting with
inet — the IP is usually 10.42.0.1 .
6. Edit fileserver.py
Open fileserver.py and change this line at the top to match your flash drive path from
Step 2:
SAVE_DIR = "/media/yourname/DRIVENAME"
7. Edit flashdrop.sh
Open flashdrop.sh and make these two changes:
Replace wlp1s0 with your WiFi interface name from Step 3
Replace 10.42.0.1 with your hotspot IP from Step 5
8. Edit showqr.py
No changes needed — it reads the QR image generated automatically.
9. Place all files in your home folder
Copy all four files to your home directory:fileserver.py
flashdrop.sh
qrwatcher.sh
showqr.py
Make the scripts executable:
chmod +x ~/flashdrop.sh ~/qrwatcher.sh
10. Create the udev rule
This makes everything trigger automatically when you plug in your flash drive.
sudo nano /etc/udev/rules.d/99-flashdrop.rules
Paste this line, replacing the UUID with yours from Step 4 and the username with your Linux
username:
ACTION=="add", ENV{ID_FS_UUID}=="YOUR-UUID-HERE", RUN+="/home/YOUR_USERNAME/flashdrop.sh"
Save and reload:
sudo udevadm control --reload-rules
11. Set up autostart
This makes the file watcher start automatically every time you log in.
mkdir -p ~/.config/autostart
nano ~/.config/autostart/qrwatcher.desktop
Paste this, replacing YOUR_USERNAME with your Linux username:
[Desktop Entry]
Type=Application
Name=QR Watcher
Exec=bash /home/YOUR_USERNAME/qrwatcher.sh
Hidden=false
NoDisplay=falseX-GNOME-Autostart-enabled=true
12. Reboot
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
