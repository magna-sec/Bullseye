# https://tcude.net/using-terraform-with-proxmox/
# DHCP ends at 169
# We hve 170-199 to use
terraform {
  required_providers {
    proxmox = {
      source = "telmate/proxmox"
      #latest version as of Nov 30 2022
      version = "2.9.11"
    }
  }
}

provider "proxmox" {
  # References our vars.tf file to plug in the api_url 
  pm_api_url = var.api_url
  # References our secrets.tfvars file to plug in our token_id
  pm_api_token_id = var.token_id
  # References our secrets.tfvars to plug in our token_secret 
  pm_api_token_secret = var.token_secret
  # Default to `true` unless you have TLS working within your pve setup 
  pm_tls_insecure = true
}

# Creates a proxmox_vm_qemu entity named blog_demo_test
resource "proxmox_vm_qemu" "wifi" {
  name ="wifi${count.index}" # count.index starts at 0
  #name = "test-vm-01"
  count = 8 # Establishes how many instances will be created 
  target_node = var.proxmox_host


  # References our vars.tf file to plug in our template name
  # Creates a full clone, rather than linked clone 
  # https://pve.proxmox.com/wiki/VM_Templates_and_Clones
  # another variable with contents "ubuntu-2004-cloudinit-template"
  clone = var.template_name
  full_clone  = "true"
 

  # VM Settings. `agent = 1` enables qemu-guest-agent
  agent = 1
  os_type = "Linux"
  cores = 2
  sockets = 1
  cpu = "host"
  memory = 2048
  scsihw = "virtio-scsi-pci"
  bootdisk = "scsi1"

  disk {
    slot = 0
    size = "50G"
    type = "scsi"
    storage = "r0-drives" # Name of storage local to the host you are spinning the VM up on
    # Enables SSD emulation
    #ssd = 1
    # Enables thin-provisioning
    discard = "on"
    #iothread = 1
  }

  network {
    model = "virtio"
    bridge = var.nic_name
    macaddr = var.mac_addresses[count.index]
  }


  lifecycle {
    ignore_changes = [
      network,
    ]
  }
  #provisioner "local-exec" {
    # Provisioner commands can be run here.
    # We will use provisioner functionality to kick off ansible
    # playbooks in the future
    #command = "touch /home/tcude/test.txt"
  #}
}

# Creates a proxmox_vm_qemu entity named blog_demo_test
resource "proxmox_vm_qemu" "ctfd" {
  name = "ctfd"
  count = 1 # Establishes how many instances will be created 
  target_node = var.proxmox_host


  # References our vars.tf file to plug in our template name
  # Creates a full clone, rather than linked clone 
  # https://pve.proxmox.com/wiki/VM_Templates_and_Clones
  # another variable with contents "ubuntu-2004-cloudinit-template"
  clone = var.template_name
  full_clone  = "true"
 

  # VM Settings. `agent = 1` enables qemu-guest-agent
  agent = 1
  os_type = "Linux"
  cores = 2
  sockets = 1
  cpu = "host"
  memory = 2048
  scsihw = "virtio-scsi-pci"
  bootdisk = "scsi1"

  disk {
    slot = 0
    size = "50G"
    type = "scsi"
    storage = "r0-drives" # Name of storage local to the host you are spinning the VM up on
    # Enables SSD emulation
    #ssd = 1
    # Enables thin-provisioning
    discard = "on"
    #iothread = 1
  }

  network {
    model = "virtio"
    bridge = var.nic_name
    macaddr = "42:CE:92:97:95:00"
  }


  lifecycle {
    ignore_changes = [
      network,
    ]
  }
  
  #provisioner "local-exec" {
    # Provisioner commands can be run here.
    # We will use provisioner functionality to kick off ansible
    # playbooks in the future
    #command = "touch /home/tcude/test.txt"
  #}
}

# Creates a proxmox_vm_qemu entity named blog_demo_test
resource "proxmox_vm_qemu" "lxc" {
  name = "lxc"
  count = 1 # Establishes how many instances will be created 
  target_node = var.proxmox_host


  # References our vars.tf file to plug in our template name
  # Creates a full clone, rather than linked clone 
  # https://pve.proxmox.com/wiki/VM_Templates_and_Clones
  # another variable with contents "ubuntu-2004-cloudinit-template"
  clone = var.template_name
  full_clone  = "true"
 

  # VM Settings. `agent = 1` enables qemu-guest-agent
  agent = 1
  os_type = "Linux"
  cores = 2
  sockets = 1
  cpu = "host"
  memory = 2048
  scsihw = "virtio-scsi-pci"
  bootdisk = "scsi1"

  disk {
    slot = 0
    size = "50G"
    type = "scsi"
    storage = "r0-drives" # Name of storage local to the host you are spinning the VM up on
    # Enables SSD emulation
    #ssd = 1
    # Enables thin-provisioning
    discard = "on"
    #iothread = 1
  }

  network {
    model = "virtio"
    bridge = var.nic_name
    macaddr = "42:CE:92:97:95:01"
  }


  lifecycle {
    ignore_changes = [
      network,
    ]
  }
  #provisioner "local-exec" {
    # Provisioner commands can be run here.
    # We will use provisioner functionality to kick off ansible
    # playbooks in the future
    #command = "touch /home/tcude/test.txt"
  #}
}