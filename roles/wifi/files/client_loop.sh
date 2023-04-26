while true; do
    wpa_supplicant -i wlan11 -c /root/wpa_supplicant_1.conf &
    sleep 45
    echo Reconnecting!
    kill $(jobs -p)
done