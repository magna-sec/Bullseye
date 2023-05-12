#!/usr/bin/python3
import subprocess
import time

def stop_vlc():
    print("Attempting to kill VLC")
    command = "kill -9 `pgrep cvlc` 2>/dev/null"
    try:
        subprocess.check_output(command, shell=True)
    except:
        print("No VLC")

def start_vlc():
    print("Starting VLC")
    try:
        command = "nohup cvlc http://192.168.64.190:8081 --play-and-exit"
        subprocess.check_output(command, shell=True)
    except:
        print("Failed to start VLC")
    


def main():
    while(True):
        stop_vlc()
        start_vlc()
        time.sleep(30)

if __name__ == "__main__":
    main()