#!/usr/bin/python3
import time
import subprocess

AMOUNT_OF_STUDENTS = 5

create_user = True
create_user_flag = "Hello There"

create_group = True
create_group_flag = "I like turtles"

user_groups = True
user_groups_flag = "Yessss"

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


    def lxc_exec(self, command):
         result = subprocess.run(command, shell=True, stdout=subprocess.PIPE)
         self.output = result.stdout.decode("utf-8")
    
    def create_user(self):
        print("SEARCH: CREATE USER")
        # Check each lxc container for their user
        for i in range(0, AMOUNT_OF_STUDENTS): 
            self.lxc_exec(f"lxc exec student{i} -- grep jedi{i} /etc/passwd")

            if(f"jedi{i}" in self.output):
                print("SUCCESS: USER EXISTS")
                self.lxc_exec(f"lxc exec student{i} -- echo {create_user_flag} >> /challenges/create_user_flag.txt")
                break

    def create_group(self):
        print("SEARCH: CREATE GROUP")
        # Check each lxc container for their group
        for i in range(0, AMOUNT_OF_STUDENTS): 
            self.lxc_exec(f"lxc exec student{i} -- grep jediorder{i} /etc/group")

            if(f"jediorder{i}" in self.output):
                print("SUCCESS: GROUP EXISTS")
                self.lxc_exec(f"lxc exec student{i} -- echo {create_group_flag} >> /challenges/create_group_flag.txt")
                break
    
    def user_groups(self):
        print("SEARCH: USER GROUPS")
        # Check each lxc container for user in group
        for i in range(0, AMOUNT_OF_STUDENTS): 
            self.lxc_exec(f"lxc exec student{i} -- groups jedi{i} | grep jediorder{i}")

            if(f"jediorder{i}" in self.output):
                print("SUCCESS: User in groups EXISTS")
                self.lxc_exec(f"lxc exec student{i} -- echo {user_groups_flag} >> /challenges/user_groups_flag.txt")
                break


def main():
    while(True):
        check = LxcCheck()
        time.sleep(60)


if __name__ == "__main__":
    main()