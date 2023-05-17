# Pi_Cluster_for_TopADD
A Raspberry Pi cluster for the TopADD program. The TopADD program can be downloaded from: https://github.com/wonderfulzzd/TopADD_2D_3D_Arbitrary_TopOpt_in_PETSc.git

The following discussion on configurations assumes one has physically built a Raspberry Pi cluster, for example: <br>
<img src="https://user-images.githubusercontent.com/19493039/236486047-83bff4b4-61f6-40b2-8cef-3ce520924f31.png" width=50% height=50%> <br>

The above cluster consists of 5 nodes, including 1 login node (in the black case) and 4 computing node.

## Method 1: Fresh installation

### 1. Download Raspberry Pi imager
https://downloads.raspberrypi.org/imager/imager_latest.exe <br>
   
   
### 2. Flash the SDs
Use Raspberry Pi imager to install OS on microSD <br>
https://www.youtube.com/watch?v=ntaXWS8Lk34 <br>
<img src="https://github.com/wonderfulzzd/Pi_Cluster_for_TopADD/assets/19493039/dcf5c17f-0098-4457-b3ee-35ff8e135bb1" width=50% height=50%> <br>


### 3. Insert the SD card and boot
Insert the microSD card/USB drive/external SSD drive to the Raspberry Pi. <br>
Connect internet cable, mouse and keyboard, monitor. <br>
Connect power supply and boot. <br>


### 4. Setup the OS

#### 4.1 Login
For Ubuntu 22.04, the default user name and password are both '**ubuntu**' if you did not create a user name and password in the Advanced options menu when flashing the SD card. <br>
You will be asked to change password immediately after you login. You may change the password to 'raspberry'. <br>

In this cluster, we set <br>
Username: **ubuntu** <br>
Password: **raspberry** <br>

#### 4.2 Change hostname
Check the hostname by:
> hostname <br>

You may want to change the hostname. <br>

Change the hostname permanently
> sudo hostnamectl set-hostname rpi0 <br>

#### 4.3 Enable SSH
For Ubuntu 20.04, the SSH seems to be enabled by default.

For other versions of Ubuntu, you may try the following steps to install and enable SSH: <br>
Install OpenSSH server program:
> sudo apt install openssh-server <br>

Check the status of the ssh server:
> sudo systemctl status ssh <br>

Use the UFW (Uncomplicated FireWall) to allow SSH connections:
> sudo ufw allow ssh <br>
> sudo ufw enable <br>

Check the UFW status:
> sudo ufw status <br>

#### 4.4 Internet connection
Check ip address:
> ip a <br>

In the section of 'eth0', you may find inet 192.168.137.118 or something like it. That is the LAN ip address of the Pi. It is created by the router DHCP server. You may want to change it to a static ip.

LAN
> sudo nano /etc/netplan/50-cloud-init.yaml <br>
Or for some other ubuntu version
> sudo nano /etc/netplan/01-network-manager-all.yaml <br>

Type the following into the file:
```
# This file is generated from information provided by the datasource.  Changes
# to it will not persist across an instance reboot.  To disable cloud-init's
# network configuration capabilities, write a file
# /etc/cloud/cloud.cfg.d/99-disable-network-config.cfg with the following:
# network: {config: disabled}
network:
    version: 2
    renderer: networkd
    ethernets:
        eth0:
            dhcp4: no
            addresses: [192.168.137.160/24]
            nameservers:
                addresses: [127.0.0.53, 8.8.8.8]
            routes:
                - to: default
                  via: 192.168.137.1
            optional: true
```

You may also want to setup and connect the WIFI:
> sudo nano /etc/netplan/01-network-manager-all.yaml <br>

Add the following into the file:
```
  wifis:
      wlan0:
          optional: true
          access-points:
              "My_wifi":
                  password: "12345678"
          dhcp4: true
```
Change "My_wifi" and password "12345678" according to a user's wifi. Pay attention to the indentation.

Then generate and apply the netplan settings：
> sudo netplan generate <br>
> sudo netplan apply <br>

Both LAN and Wifi should have been connected.

If you want to prioritize wifi connection over ethernet connection, you have to do as following steps: <br>
Pull off the ethernet cable and reboot. You will have internet connection through wifi. <br>
> sudo apt install net-tools <br>
> sudo apt install ifmetric <br>
> route -n <br>

You may see something similar to the following info: <br>
```
Destination     Gateway     Genmask       Flags       Metric       Ref      Use     Iface
0.0.0.0        192.168.137.1  0.0.0.0      UG         0            0        0       eth0 
0.0.0.0        192.168.43.1   0.0.0.0      UG         600          0        0       wlan0
```
> sudo ifmetric eth0 700 <br>

After doing the above, priority will be changed to: <br>
```
Destination     Gateway     Genmask       Flags       Metric       Ref      Use     Iface
0.0.0.0        192.168.43.1   0.0.0.0      UG         600          0        0       wlan0
0.0.0.0        192.168.137.1  0.0.0.0      UG         700          0        0       eth0
```

#### 4.5 Change hosts
Hosts are the hosts ip and names for your other nodes in the cluster. You may want to change the hosts, which will be the ip and hostname for the other nodes in the cluster. The hosts can be changed as follows: <br>
> sudo nano /etc/hosts <br>

You can set them up by typing the following into the above file:
```
127.0.0.1 localhost

192.168.137.160 rpi0
192.168.137.161 rpi1
192.168.137.162 rpi2
192.168.137.163 rpi3
192.168.137.164 rpi4

# The following lines are desirable for IPv6 capable hosts
::1 ip6-localhost ip6-loopback
fe00::0 ip6-localnet
fe00::0 ip6-mcastprefix
fe00::1 ip6-allnodes
fe00::2 ip6-allrouters
fe00::3 ip6-allhosts
```

Before update the OS, we need to reboot the rpi. <br>
> sudo reboot <br>


#### 4.6 Update the OS
Before update the OS, it may need to reboot. Otherwise, error of 
> sudo apt-get update <br>

#### 4.7 Install make 
"make" is used to build groups of programs from the source code.
> sudo apt-get install make <br>

#### 4.8 MPICH
> sudo apt-get install mpich <br>

#### 4.9 Install libblas liblapack
Lapack is a standard software library for numerical linear algebra. It relies on BLAS implementation.
Install
> sudo apt-get install libblas-dev liblapack-dev <br>

#### 4.10 Install hypre
Download hypre
> mkdir opt <br>
> cd top <br>
> wget -c https://github.com/hypre-space/hypre/archive/refs/tags/v2.19.0.tar.gz <br>

Install hypre
> tar -xof v2.19.0.tar.gz <br>
> cd hypre-2.19.0/src <br>
> ./configure --prefix=/home/ubuntu/opt/hypre-2.19.0 --enable-shared <br>
> make -j4 install <br>

#### 4.11 Install PETSc
The official instruction: <br>
https://petsc.org/main/install/install/ <br>

Download PETSc
> cd ~/ubuntu/opt
> wget -c https://ftp.mcs.anl.gov/pub/petsc/release-snapshots/petsc-3.16.3.tar.gz <br>

Install PETSc. <br>
> tar -xof petsc-3.16.3.tar.gz <br>
> cd petsc-3.16.3 <br>
> ./configure PETSC_DIR=/home/ubuntu/opt/petsc-3.16.3 PETSC_ARCH=arch-linux-mpicc-release --COPTFLAGS='-O3' --CXXOPTFLAGS='-O3' --FOPTFLAGS='-O3' --with-hypre-dir=/home/ubuntu/opt/hypre-2.19.0 --with-debugging=0 --with-cc=mpicc --with-cxx=mpicxx --with-fc=mpif90  <br>
> make -j4 PETSC_DIR=/home/ubuntu/opt/petsc-3.16.3 PETSC_ARCH=arch-linux-mpicc-release all <br>


### 5. Clone multiple microSD
Use an open-source software called Clonezilla: https://clonezilla.org/
Tutorial can be found: https://clonezilla.org/fine-print-live-doc.php?path=clonezilla-live/doc/03_Disk_to_disk_clone


### 6. Change the hostname and IP addresses accordingly
For other nodes, change the hostname accordingly, for example rpi1:
> sudo hostnamectl set-hostname rpi1 <br>

Change the IP address <br>
> sudo nano /etc/netplan/50-cloud-init.yaml <br>

Or for some other ubuntu version <br>
> sudo nano /etc/netplan/01-network-manager-all.yaml <br>

For example: <br>
192.168.137.161 for rpi1 <br>
192.168.137.162 for rpi2 <br>
192.168.137.163 for rpi3 <br>
192.168.137.164 for rpi4 <br>


### 7. Set up password-less SSH login
Enable to login to a remote computer via ssh without having to enter the password
Go to .ssh directory <br
> cd ~/.ssh <br>

Generate a SSH key <br>
> ssh-keygen <br>

Press the "enter" button three times. <br> 

Copy the key to each remote desktop, e.g rpi1 <br>
> ssh-copy-id ubuntu@rpi1 <br>

Test the setup whether is successful <br>
> ssh ubuntu@rpi1 <br>


### 8. Network file system (NFS)
A shared storage is needed on a cluster when each node needs to be able to access the same files. This can be achieved by setting up a Network File System (NFS).

#### 8.1 Check the identifier of the drive:
Insert a flash drive or SSD drive into one of the USB prots on the master node. Then, find the drive's identifier by lsblk
> lsblk
```
NAME        MAJ:MIN RM   SIZE RO TYPE MOUNTPOINTS
loop0         7:0    0  59.1M  1 loop /snap/core20/1826
loop1         7:1    0  59.1M  1 loop /snap/core20/1883
loop2         7:2    0 109.6M  1 loop /snap/lxd/24326
loop3         7:3    0  43.2M  1 loop /snap/snapd/18363
sda           8:0    1 114.6G  0 disk
└─sda1        8:1    1 114.6G  0 part
mmcblk0     179:0    0 119.4G  0 disk
├─mmcblk0p1 179:1    0   256M  0 part /boot/firmware
└─mmcblk0p2 179:2    0 119.1G  0 part /
```
So the drive identifier is /dev/sda1

#### 8.2 Format the drive
> sudo mkfs.ext4 /dev/sda1

#### 8.3 Create the mount directory
Create a directory, e.g. /clusterfs, and make its permission level below to anyone by setting nobody:nogroup. Also enable it to do all operations, e.g. write, read, execute by setting chmod 777.
> sudo mkdir /clusterfs <br>
> sudo chown nobody:nogroup -R /clusterfs <br>
> sudo chmod 777 -R /clusterfs

#### 8.4 Setup automatic mounting
It is required to get the UUID of the drive in order to do automatic mounting.
> blkid <br>
```
/dev/sda1: UUID="2defec4b-334c-4b3e-ad7f-aab5c2a5a785" BLOCK_SIZE="4096" TYPE="ext4" PARTUUID="70d094fc-01"
```

Now edit /etc/fstab to mount the drive automatically.
> sudo nano /etc/fstab <br>

Add the following line:
```
#device                                    mountpoint fstype options dump fsck
UUID=2defec4b-334c-4b3e-ad7f-aab5c2a5a785 /clusterfs ext4 defaults 0 2
```

Note: <br>
dump of 0 will assume that the filesystem does not need to be dumped.
fsck should be 2 for not root partition.

Finally mount
> sudo mount -a

#### 8.5 Install NFS server
In this step run the below command in Ubuntu 20.04 terminal for NFS server installation.
> sudo apt install nfs-kernel-server <br>

#### 8.6 Grant NFS access
In this step, we will grant access to the client system.
> sudo nano /etc/exports
```
/clusterfs 192.168.137.160/24(rw,sync,no_root_squash,no_subtree_check)
```

#### 8.7 Exporting NFS 
> sudo exportfs -a

#### 8.8 Grant Firewall access
Allow the Firewall access for connections within the subnet of 192.168.137.0/24. On each node, run the following command:
> sudo ufw allow from 192.168.137.0/24 <br>
> sudo ufw enable <br>
> sudo ufw status <br>
```
Status: active

To                         Action      From
--                         ------      ----
22/tcp                     ALLOW       Anywhere
Anywhere                   ALLOW       192.168.137.0/24
22/tcp (v6)                ALLOW       Anywhere (v6)
```

#### 8.9 Install NFS on other nodes
> sudo apt-get install nfs-common <br>
> sudo mkdir /clusterfs <br>
> sudo chown nobody:nogroup /clusterfs
> sudo chmod -R 777 /clusterfs

#### 8.10 Setup automatic mounting on other nodes
Now edit /etc/fstab to mount the drive automatically.
> sudo nano /etc/fstab <br>

Add the following line:
```
#device                                    mountpoint fstype options dump fsck
192.168.137.160:/clusterfs  /clusterfs  nfs nofail,x-systemd.automount,x-systemd.requires=network-online.target,x-systemd.device-timeout=10 0 0
```
> sudo mount -a <br>

Reference: <br>
https://glmdev.medium.com/building-a-raspberry-pi-cluster-784f0df9afbd <br>
https://linuxhint.com/install-and-configure-nfs-server-ubuntu-22-04/   <br>

### 9. Try run the TopADD program
Clone the TopADD repo on github
> cd /clusterfs
> git clone https://github.com/wonderfulzzd/TopADD_2D_3D_Arbitrary_TopOpt_in_PETSc.git <br>
> cd TopADD_2D_3D_Arbitrary_TopOpt_in_PETSc <br>

Change the PETSC_DIR and PETSC_ARCH in the makefile accordingly
> nano makefile <br>
```
PETSC_DIR=/home/ubuntu/opt/petsc-3.16.3
PETSC_ARCH=arch-linux-mpicc-release
```

Add a machine file in order to run it in parallel
> nano machinefile
```
rpi1
rpi2
rpi3
rpi4
```

Compile and run
> make -j4 topopt <br>
> mpiexec -n 16 -hostfile machinefile ./topopt

The cluster has been successfully configured.


### 10. (optional) Ubuntu desktop

#### 10.1 Install Ubuntu desktop
If you prefer a UI eniveroment, you can install an ubuntu-desktop on the login node. <br>
> sudo reboot <br>
> sudo apt update <br>
> sudo apt install ubuntu-desktop <br>

#### 10.2 Install paraview
In order to postprocessing the topology optimization results, paraview is required to be installed. <br>

Install paraview by: <br>
> sudo apt install paraview-dev <br>

#### 10.3 Enable screen sharing
If Ubuntu desktop is installed on a Raspberry Pi, then the Pi can be remotelly controlled. <br>
<img src="https://user-images.githubusercontent.com/19493039/236723444-743861a7-bd64-4de4-8e89-32581a72d0b0.png" width=80% height=80%> <br>
<img src="https://user-images.githubusercontent.com/19493039/236728172-8e493577-d68f-4e60-b645-2ea88bf02a1d.png" width=80% height=80%> <br>

Install TightVNC Viewer on a Windows laptop/desktop. Connect the laptop to the switch connecting the Pi.
<img src="https://user-images.githubusercontent.com/19493039/237030336-ff45598e-e2f2-4481-aa05-497b94137b35.png" width=50% height=50%> <br>

Note: to share the media, networkmanager need to be enable. So change the renderer from "networkd" to "NetworkManager" in the netplan configuration file. <br>
> sudo nano /etc/netplan/01-network-manager-all.yaml <br> 

```
# This file is generated from information provided by the datasource.  Changes
# to it will not persist across an instance reboot.  To disable cloud-init's
# network configuration capabilities, write a file
# /etc/cloud/cloud.cfg.d/99-disable-network-config.cfg with the following:
# network: {config: disabled}
network:
    version: 2
#    renderer: networkd
    renderer: NetworkManager
    ethernets:
        eth0:
            dhcp4: false
            addresses: [192.168.137.160/24]
            nameservers:
                addresses: [127.0.0.53, 8.8.8.8]
            routes:
                - to: default
                  via: 192.168.137.1
            optional: true
            
    wifis:
        wlan0:
            optional: true
            access-points:
                "My_wifi":
                    password: "12345678"
            dhcp4: true
```
There is one more pitfall. When we try to remotely control, the error message may be received 
<img src="https://github.com/wonderfulzzd/Pi_Cluster_for_TopADD/assets/19493039/99a8d875-3dbd-4bac-a69a-7d71aff81fbe" width=50% height=50%> <br>

This error can be corrected by disable the encryption of the Vino server. Vino server is taking in charge of the screen sharing. <br>
> gsettings set org.gnome.Vino require-encryption false <br>

#### 10.4 Enable auto login
If you prefer to use ubuntu without typing the password every time, auto login can be enabled. <br>
> sudo nano /etc/gdm3/custom.conf <br>

Uncomment the following two lines. <br>
```
AutomaticLoginEnable=true
AutomaticLogin=ubuntu
```

#### 10.5 Turn off blank screen functionality
To keep the screen always on, we can do the following. Change the blank screen to "Never". <br>
<img src="https://github.com/wonderfulzzd/Pi_Cluster_for_TopADD/assets/19493039/4148d208-2025-4ed2-a2cb-ffb0a0e3e283" width=50% height=50%> <br>


#### 10.5 Update mpi priority
After installing paraview, another version of mpi, called OpenMPI will be automatically install. This will interference with the previously install mpich. So like when we compile the topopt program <br>
> make -j4 topopt <br>

We may get the error message: <br>
```
# error "PETSc was configured with MPICH but now appears to be compiling using a non-MPICH mpi.h"
```

This error shows up because the OpenMPI has a higher priority than MPICH. This can be confirmed by <br>
> update-alternatives --query mpi <br>

We can manually select mpich as the mpi library by: <br>
> sudo update-alternatives --config mpi <br>

Then type the selection number: 1 to use mpich in manual mode. <br>
<img src="https://github.com/wonderfulzzd/Pi_Cluster_for_TopADD/assets/19493039/3045e4b4-c6dc-4dfa-a418-e64d154f4adb" width=50% height=50%> <br>


#### 10.6 Install python2
To process the generated topology optimization results, python2 should be install by <br>
> sudo apt install python2 <br>

#### 10.7 Restart
Restart the system <br>
> sudo reboot <br>


## Method 2: Restore from the provided image files
### 1. Download the saved OS image file
   https://drive.google.com/file/d/1a3AGSDZsX-cr1Yr_Lzr8m-sxWUnLC_gN/view?usp=share_link
   
### 2. Restore the image file on microSD cards
   Use an open-source software called Clonezilla: https://clonezilla.org/
   Tutorial can be found: https://clonezilla.org/fine-print-live-doc.php?path=clonezilla-live/doc/03_Disk_to_disk_clone

### 3. Insert the SD card and boot
Insert the microSD card/USB drive/external SSD drive to the Raspberry Pi. <br>
Connect internet cable, mouse and keyboard, monitor. <br>
Connect power supply and boot. <br>

### 4. Follow the step 6-10 in Method 1

