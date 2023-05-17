#!/usr/bin/python3
from smb.SMBConnection import SMBConnection

# File
send_file = "cat.jpg"

# Credentials
userID = 'smbuser'
password = 'Passw0rd!'

# Settings
client_machine_name = 'client'
sharename = "print"
server_name = 'ctfd'
domain_name = server_name
server_ip = '192.168.64.190'

# File list
file_obj = open(send_file, 'rb')

# Make connection
conn = SMBConnection(userID, password, client_machine_name, server_name, domain=domain_name, use_ntlm_v2=True,is_direct_tcp=True)
conn.connect(server_ip, 445)

# Send file
conn.storeFile(service_name=sharename, path=f"\{send_file}",file_obj=file_obj)

