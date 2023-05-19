#!/usr/bin/python3
import telnetlib
import time

host = "192.168.64.190"
user = "telnet"
password = "Passw0rd!"
flag = "epidiascope"

def telnet_send():
    # Connect and wait
    tn = telnetlib.Telnet()
    time.sleep(5)

    # Login
    tn.open(host)
    tn.read_until(b"login: ")
    tn.write(user.encode("ascii") + b"\n")
    tn.read_until(b"Password: ")
    tn.write(password.encode("ascii") + b"\n")

    # Create folder
    tn.write(b"mkdir ~/Documents\n")
    time.sleep(5)
    # Create file
    tn.write (b"touch ~/Documents/" + flag.encode("ascii") + b"\n")
    time.sleep(10)
    # Move
    tn.write(b"cd ~/\n")
    # Remove folder
    tn.write(b"rm -r ~/Documents\n")
    print (tn.read_some())
    time.sleep(10)

    # Run away
    tn.write(b"exit\n")
    tn.close()



def main():
    while(True):
        telnet_send()
        time.sleep(30)

if __name__ == "__main__":
    main()
