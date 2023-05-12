#!/usr/bin/python3
import time
import subprocess

AMOUNT_OF_USERS = "5"
SCR_USER = "scr"

create_user = True
create_user_flag = "patronised"

create_group = True
create_group_flag = "preplanned"

user_groups = True
user_groups_flag = "prebendary"

folder_perms = True
#640: gread, 620: gwrite,604: pread,602: pwrite
folder_perms_check = "620"
folder_perms_flag = "Tosephtas"


class LxcCheck:
    def __init__(self):
        self.output = ""
        self.start_check()

    
    def start_check(self):
        if(create_user):
            self.create_user()
        if(create_group):
            self.create_group()
        if(user_groups):
            self.user_groups()
        if(folder_perms):
            self.folder_perms()


    def lxc_exec(self, command):
         result = subprocess.run(command, shell=True, stdout=subprocess.PIPE)
         self.output = result.stdout.decode("utf-8")
    
    def create_user(self):
        # Check each lxc container for their user
        for i in range(0, int(AMOUNT_OF_USERS)): 
            print("Checking {i}: Create user")
            self.lxc_exec(f"lxc exec user{i} -- grep jedi{i} /etc/passwd")

            if(f"jedi{i}" in self.output):
                print("SUCCESS: USER EXISTS")
                self.lxc_exec(f"lxc exec user{i} -- bash -c 'echo {create_user_flag} > /home/{SCR_USER}/challenges/create_user_flag.txt'")

    def create_group(self):
        # Check each lxc container for their group
        for i in range(0, int(AMOUNT_OF_USERS)): 
            print("Checking {i}: Create Group")
            self.lxc_exec(f"lxc exec user{i} -- grep jediorder{i} /etc/group")

            if(f"jediorder{i}" in self.output):
                print("SUCCESS: GROUP EXISTS")
                self.lxc_exec(f"lxc exec user{i} -- bash -c 'echo {create_group_flag} > /home/{SCR_USER}/challenges/create_group_flag.txt'")
    
    def user_groups(self):
        # Check each lxc container for user in group
        for i in range(0, int(AMOUNT_OF_USERS)): 
            print("Checking {i}: Add2Group")
            self.lxc_exec(f"lxc exec user{i} -- groups jedi{i} | grep jediorder{i}")

            if(f"jediorder{i}" in self.output):
                print("SUCCESS: User in groups EXISTS")
                self.lxc_exec(f"lxc exec user{i} -- bash -c 'echo {user_groups_flag} > /home/{SCR_USER}/challenges/user_groups_flag.txt'")

    def folder_perms(self):
        # Check each lxc container for directory perms
        for i in range(0, int(AMOUNT_OF_USERS)):
            print("Checking {i}: Folder Perms")
            self.lxc_exec(f"lxc exec user{i} -- stat -c '%a' /home/{SCR_USER}/PermMe/")

            if(self.output.strip() == folder_perms_check):
                print("SUCCESS: Folder Perms correct")
                self.lxc_exec(f"lxc exec user{i} -- bash -c 'echo {folder_perms_flag} > /home/{SCR_USER}/challenges/folder_perms_flag.txt'")



def main():
    while(True):
        check = LxcCheck()
        time.sleep(60)


if __name__ == "__main__":
    main()