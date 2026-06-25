FlashDrop
Wirelessly send and receive files to/from a USB flash drive using your phone, no internet,
no app, no cables.
How it works
1. Plug in your flash drive
2. Your PC automatically creates a WiFi hotspot
3. A QR code pops up on screen
4. Connect your phone to the hotspot and scan the QR code
5. Browser opens — upload files to the drive or download files from it
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
python3-tk
Setup1. Install dependencies
sudo apt install qrencode python3-tk -y
2. Find your flash drive path
lsblk
Note the mount path e.g. /media/yourname/DRIVEID
3. Edit fileserver.py
Change this line to match your flash drive path:
SAVE_DIR = "/media/yourname/DRIVEID"
4. Edit flashdrop.sh
Change wlp1s0 to your WiFi interface name. Find it with:
ip link
5. Find your flash drive UUID
lsblk -o NAME,UUID,LABEL
6. Create udev rule
sudo nano /etc/udev/rules.d/99-flashdrop.rules
Paste this inside, replacing the UUID and username:
ACTION=="add", ENV{ID_FS_UUID}=="YOUR-UUID-HERE", RUN+="/home/yourname/flashdrop.sh"
Then reload:
sudo udevadm control --reload-rules
7. Set up autostartmkdir -p ~/.config/autostart
nano ~/.config/autostart/qrwatcher.desktop
Paste this inside, replacing yourname with your Linux username:
[Desktop Entry]
Type=Application
Name=QR Watcher
Exec=bash /home/yourname/qrwatcher.sh
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
8. Make scripts executable
chmod +x ~/flashdrop.sh ~/qrwatcher.sh
9. Reboot
After rebooting, plug in your flash drive and everything starts automatically.
Usage
Send to Drive — tap the file picker, select multiple files, tap Send
Get from Drive — switch to the second tab, browse files on the drive, tap Download to
save to your phone
Notes
Works on any phone browser — no app needed
Hotspot name: FileDrop , password: 12345678 (change in flashdrop.sh)
Files save directly to the flash drive root folder
Server runs on http://10.42.0.1:8080
Author
Built by Joe — @EligibleFreak
