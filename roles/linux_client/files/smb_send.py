#!/usr/bin/python3
from smb.SMBConnection import SMBConnection
import time

# File
send_path = "/home/smbuser/cat.jpg"
send_name = send_path.split('/')[3]

# Credentials
userID = 'smbuser'
password = 'Passw0rd!'

# Settings
client_machine_name = 'client'
sharename = "print"
server_name = 'ctfd'
domain_name = server_name
server_ip = '192.168.64.190'

def send_file():
    # File list
    file_obj = open(send_path, 'rb')

    # Make connection
    conn = SMBConnection(userID, password, client_machine_name, server_name, domain=domain_name, use_ntlm_v2=True,is_direct_tcp=True)
    conn.connect(server_ip, 445)

    # Send file
    conn.storeFile(service_name=sharename, path=f"\{send_name}",file_obj=file_obj)
    file_obj.close()
    print("## File Sent ##")
    


def main():
    while(True):
        send_file()
        time.sleep(30)

if __name__ == "__main__":
    main()

