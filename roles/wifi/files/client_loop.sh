while true; do
    wpa_supplicant -i wlan30 -c /root/wpa_supplicant.conf &
    sleep 45
    echo Reconnecting!
    pkill wpa_supplicant
done