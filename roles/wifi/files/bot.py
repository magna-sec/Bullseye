#!/usr/bin/python3
import time
import subprocess

join_wifi = "True"
join_wifi_flag = "pseudobrachium"


class LxcCheck:
    def __init__(self):
        self.output = ""
        self.ssid = ""
        self.start_check()

    
    def start_check(self):
        if(join_wifi):
            self.get_wifi_name()
            self.wifi_joined()
    
    def get_wifi_name(self):
        print("Searching for WiFi name")
        command = f"cat /root/wpa_supplicant_1.conf  | grep ssid | cut -d '\"' -f 2"
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE)
        self.ssid = result.stdout.decode("utf-8").strip()  

    def wifi_joined(self):
        print("SEARCH: WiFI joined")
        command = f"iwconfig wlan0"
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE)
        self.output = result.stdout.decode("utf-8")
        if(self.ssid in self.output):
            print("SUCCESS: WiFi Found")
            command = f"echo {join_wifi_flag} > /home/scr/join_wifi_flag.txt"
            result = subprocess.run(command, shell=True, stdout=subprocess.PIPE)

def main():
    while(True):
        check = LxcCheck()
        time.sleep(60)


if __name__ == "__main__":
    main()