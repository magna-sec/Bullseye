import telnetlib
import time


host = "192.168.64.190"
user = "telnet"
password = "Passw0rd!"


n = 0
while n < 1:
    tn = telnetlib.Telnet()
    time.sleep(5)
    tn.open(host)
    tn.read_until(b"login: ")
    tn.write(user.encode("ascii")+b"\n")
    tn.read_until(b"Password: ")
    tn.write(password.encode("ascii")+b"\n")
    tn.write(b"mkdir ~/Documents\n")
    time.sleep(5)
    tn.write (b"touch ~/Documents/hello\n")
    time.sleep(10)
    tn.write(b"cd ~/\n")
    tn.write(b"rm -r ~/Documents\n")
    print (tn.read_some())
    time.sleep(10)
    tn.write(b"exit\n")
    tn.close()
    n+=1
