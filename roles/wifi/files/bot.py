#!/usr/bin/python3
import time
import subprocess

join_wifi = "True"
join_wifi_flag = "backstretches"
client_password = "phosphorescing"

class WiFiCheck:
    def __init__(self):
        self.output = ""
        self.ssid = ""
        self.joined = False
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
        print("SEARCH: WiFi joined")
        command = "iwconfig wlan0"
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE)
        self.output = result.stdout.decode("utf-8")
        if(self.ssid in self.output):
            print("SUCCESS: WiFi Found")
            self.joined = True
            # Give flag
            command = f'echo "{join_wifi_flag}" > /home/scr/join_wifi_flag.txt'
            result = subprocess.run(command, shell=True, stdout=subprocess.PIPE)
            # Give password
            command = f'echo "Well done! Now connect to 192.168.64.188 as scr:{client_password}" > /home/scr/client_password.txt'
            result = subprocess.run(command, shell=True, stdout=subprocess.PIPE)

            
        else:
            self.joined = False

def main():
    while(True):
        check = WiFiCheck()
        time.sleep(60)


if __name__ == "__main__":
    main()