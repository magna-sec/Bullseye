#!/usr/bin/python3
import time
import subprocess

join_wifi = "True"
join_wifi_flag = "narrative's"


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
            self.view_stream()

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
            command = f'echo "{join_wifi_flag}" > /home/scr/join_wifi_flag.txt'
            result = subprocess.run(command, shell=True, stdout=subprocess.PIPE)
        else:
            self.joined = False

    def view_stream(self):
        while(self.joined):
            time.sleep(10)
            self.wifi_joined()
            print("HI")

def main():
    while(True):
        check = WiFiCheck()
        time.sleep(60)


if __name__ == "__main__":
    main()