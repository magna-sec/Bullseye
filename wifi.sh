#!/bin/bash
WIFI_1_Name="Hello There"
WIFI_1_PW="summer2018"
# Setting up the interfaces
# get the dependencies
apt install wpasupplicant hostapd aircrack-ng wireless-tools

# Disable the default wpa_supplicant service, we'll be starting a client ourselves
systemctl stop wpa_supplicant.service
systemctl disable wpa_supplicant.service

# Create the network interfaces
modprobe mac80211_hwsim radios=3

# Set up the module to be loaded on boot
echo 'mac80211_hwsim' >> /etc/modules-load.d/vwifi.conf
echo 'options mac80211_hwsim radios=3' >> /etc/modprobe.d/vwifi.conf


# Setting up the AP
ip addr add 192.168.21.1/24 dev wlan1 # Assign a static IP to the card, not really used since there's no traffic but could be in the future

# Output hostapd config file
cat <<EOF >/root/hostapd.conf
interface=wlan1
driver=nl80211
country_code=UK
ssid=$WIFI_1_Name
channel=0
hw_mode=b
wpa=3
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP CCMP
wpa_passphrase=$WIFI_1_PW
auth_algs=3
beacon_int=100
EOF

# Output a DHCP+hostapd script
cat << EOF > /root/ap_setup.sh
hostapd /root/hostapd.conf &
EOF
chmod +x /root/ap_setup.sh

# Setting up the bot client
cat << EOF > /root/wpa_supplicant.conf
network={
  ssid="$WIFI_1_Name"
  key_mgmt=WPA-PSK
  psk="$WIFI_1_PW"
}
EOF

cat << EOF > /root/client_loop.sh
while true; do
    wpa_supplicant -i wlan2 -c /root/wpa_supplicant.conf &
    sleep 45
    echo Reconnecting!
    pkill wpa_supplicant
done
EOF

chmod +x /root/client_loop.sh

# Set up the AP and client to run on autostart
cat << EOF > /root/autostart.sh
#!/bin/bash
nohup bash /root/ap_setup.sh &
nohup bash /root/client_loop.sh &
EOF
chmod +x /root/autostart.sh

cat << EOF > /etc/systemd/system/virtual-wifi.service
[Unit]
Description=Virtual Wifi AP&Client

[Service]
Type=oneshot
ExecStart=/root/autostart.sh
RemainAfterExit=true
StandardOutput=journal

[Install]
WantedBy=default.target
EOF

systemctl enable virtual-wifi.service
reboot now

# Setting up the attacker container
# Useful guide for forwarding interfaces: https://blog.simos.info/using-the-lxd-kali-container-image/
lxd init

lxc launch images:alpine/3.11 attacker

# Do some updating on the container and set up ssh server on the container
# Drop into a shell into the container, commands following will be run in the container until we exit it
lxc config set attacker boot.autostart true
lxc exec attacker -- /bin/ash
apk update
apk upgrade
apk add iw aircrack-ng openssh

vi /etc/ssh/sshd_config # Allow root password auth
rc-update add sshd
/etc/init.d/sshd start
echo 'root:Tryhackme123!' | chpasswd
exit

# Set up a port forward for ssh
lxc config device add attacker sshproxy proxy listen=tcp:0.0.0.0:2222 connect=tcp:127.0.0.1:22

# Remove the default bridge device (internet/network access)
lxc config device add attacker eth0 none
# Add the bridge device back
lxc config device remove attacker eth0

# Set up wireless networking on the container
lxc config device add attacker wifi nic nictype=physical parent=wlan0 name=wlan0

# Drop back into the container
lxc exec attacker -- /bin/ash
# Check if we can start/stop monitor mode on the interface now
airmon-ng check wlan0
airmon-ng start wlan0
airmon-ng stop wlan0mon
exit