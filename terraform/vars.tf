#Set your public SSH key here
variable "ssh_key" {
  default = "your_public_ssh_key_here"
}
#Establish which Proxmox host you'd like to spin a VM up on
variable "proxmox_host" {
    default = "p2"
}
#Specify which template name you'd like to use
variable "template_name" {
    default = "p2jammy"
}
#Establish which nic you would like to utilize
variable "nic_name" {
    default = "vmbr0"
}
#Establish the VLAN you'd like to use
variable "vlan_num" {
    default = "place_vlan_number_here"
}
#Provide the url of the host you would like the API to communicate on.
#It is safe to default to setting this as the URL for what you used
#as your `proxmox_host`, although they can be different
variable "api_url" {
    default = "https://p2.dcxl.xz:8006/api2/json"
}
variable "amount_of_users" {
    type = number
    default = 3
}
#Blank var for use by terraform.tfvars
variable "token_secret" {
}
#Blank var for use by terraform.tfvars
variable "token_id" {
}

variable "mac_addresses" {
    type = list(string)
    default = [
        "42:CE:92:97:95:02",
        "42:CE:92:97:95:03",
        "42:CE:92:97:95:04",
        "42:CE:92:97:95:05",
        "42:CE:92:97:95:06",
        "42:CE:92:97:95:07",
        "42:CE:92:97:95:08",
        "42:CE:92:97:95:09",
        "42:CE:92:97:95:0A",
        "42:CE:92:97:95:0B",
        "42:CE:92:97:95:0C",
        "42:CE:92:97:95:0D",
        "42:CE:92:97:95:0E",
        "42:CE:92:97:95:0F",
        "42:CE:92:97:95:10",
        "42:CE:92:97:95:11",
        "42:CE:92:97:95:12",
        "42:CE:92:97:95:13",
        "42:CE:92:97:95:14",
        "42:CE:92:97:95:15",
        "42:CE:92:97:95:16",
        "42:CE:92:97:95:17",
    ]
  
}
