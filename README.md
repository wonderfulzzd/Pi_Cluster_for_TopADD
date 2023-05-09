# Pi_Cluster_for_TopADD
A Raspberry Pi cluster for the TopADD program

The following discussion on configurations assumes one has physically built a Raspberry Pi cluster, for example: <br>
<img src="https://user-images.githubusercontent.com/19493039/236486047-83bff4b4-61f6-40b2-8cef-3ce520924f31.png" width=50% height=50%>

The above cluster consists of 5 nodes, including 1 login node (in the black case) and 4 computing node.

## Method 1: Fresh installation

### 1. Download Raspberry Pi imager
https://downloads.raspberrypi.org/imager/imager_latest.exe <br>
   
### 2. Flash the SDs
Use Raspberry Pi imager to install OS on microSD <br>
https://www.youtube.com/watch?v=ntaXWS8Lk34 <br>
<img src="https://user-images.githubusercontent.com/19493039/236716118-559bbcb7-0bce-4ec0-99e0-819e191e2d1e.png" width=50% height=50%>

<img src="https://user-images.githubusercontent.com/19493039/236950684-e8c50b4f-6f36-4516-915d-f12aaea5950a.png" width=50% height=50%>


### 3. Insert the SD card and boot
Insert the microSD card/USB drive/external SSD drive to the Raspberry Pi. <br>
Connect internet cable, mouse and keyboard, monitor. <br>
Connect power supply and boot.


### 4. Setup the OS

#### 4.1 Login
For Ubuntu 22.04, the default user name and password are both 'ubuntu' if you did not create a user name and password in the Advanced options menu when flashing the SD card. <br>
You will be asked to change password immediately after you login. You may change the password to 'raspberry'. <br>

#### 4.1 Change hostname
Check the hostname by:
> hostname

You may want to change the hostname. <br>

Change the hostname permanently
> sudo hostnamectl set-hostname rpi0

#### 4.2 Enable SSH
For Ubuntu 22.04, the SSH seems to be enabled by default.

For other versions of Ubuntu, you may try the following steps to install and enable SSH: <br>
Install OpenSSH server program:
> sudo apt install openssh-server 

Check the status of the ssh server:
> sudo systemctl status ssh

Use the UFW (Uncomplicated FireWall) to allow SSH connections:
> sudo ufw allow ssh
> sudo ufw enable

Check the UFW status:
> sudo ufw status

#### 4.3 Internet connection
Check ip address:
> ip a

In the section of 'eth0', you may find inet 192.168.137.118 or something like it. That is the LAN ip address of the Pi. It is created by the router DHCP server. You may want to change it to a static ip.

LAN
> sudo nano /etc/netplan/01-network-manager-all.yaml

Type the following into the file:
```
# This file is generated from information provided by the datasource.  Changes
# to it will not persist across an instance reboot.  To disable cloud-init's
# network configuration capabilities, write a file
# /etc/cloud/cloud.cfg.d/99-disable-network-config.cfg with the following:
# network: {config: disabled}
network:
    version: 2
    ethernets:
        eth0:
            dhcp4: no
            addresses: [192.168.137.161/24]
            nameservers:
                addresses: [127.0.0.53, 8.8.8.8]
            routes:
                - to: default
                  via: 192.168.137.1
            optional: true
```

You may also want to setup and connect the WIFI:
> sudo nano /etc/netplan/01-network-manager-all.yaml

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


You may want to change the hosts, which will be the ip and hostname for the other nodes in the cluster. The hosts can be changed as follows:
> sudo nano /etc/hosts

#### 4.4 Change hosts
Hosts are the hosts ip and names for your other nodes in the cluster. You can check them in /etc/hosts. <br>
> sudo /etc/hosts


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
#### 4.5 Update OS
> sudo apt-get update

#### 4.5 Install make 
"make" is used to build groups of programs from the source code.
> sudo apt install make

#### 4.6 MPICH
> sudo apt install mpich

#### 4.5 Install hypre
Download hypre
> wget -c https://github.com/hypre-space/hypre/archive/refs/tags/v2.19.0.tar.gz -O hypre-2.19.0.tar.gz

Install hypre
> tar -xof hypre-2.19.0.tar.gz
> cd hypre-2.19.0/src
> ./configure --prefix=/home/ubuntu/opt --enable-shared
> make -j4 install

#### 4.7 PETSc
On the NAS directory from step 3.1, called "clusterfs", install the software PETSc. <br>
The official instruction: <br>
https://petsc.org/main/install/install/ <br>
The configuration I used: <br>
> ./configure PETSC_DIR=/home/ubuntu/opt/petsc-3.10.2 PETSC_ARCH=arch-linux-mpicc-release --COPTFLAGS='-O3' --CXXOPTFLAGS='-O3' --FOPTFLAGS='-O3' --with-hypre-dir=/clusterfs/opt/hypre-2.14.0 --with-debugging=0 --with-cc=mpicc --with-cxx=mpicxx --with-fc=mpif90  <br>

#### 4.3 (optional if install ubuntu desktop) Enable screen sharing
Connect a laptop to the switch <br>
<img src="https://user-images.githubusercontent.com/19493039/236723444-743861a7-bd64-4de4-8e89-32581a72d0b0.png" width=50% height=50%>
<img src="https://user-images.githubusercontent.com/19493039/236728172-8e493577-d68f-4e60-b645-2ea88bf02a1d.png" width=50% height=50%>


### 5. Clone multiple microSD
Use an open-source software called Clonezilla: https://clonezilla.org/
Tutorial can be found: https://clonezilla.org/fine-print-live-doc.php?path=clonezilla-live/doc/03_Disk_to_disk_clone

### 6. Change the hostname accordingly
For other nodes, change the hostname accordingly, for example rpi1:
> sudo hostnamectl set-hostname rpi1

### 7. Try run the TopADD program


## Method 2: Restore from the provided image files
### 1. Download the provided image files
   https://drive.google.com/drive/folders/1AKukyrJqC8yL2S2H1plEN8ZqoN_B8zXJ?usp=share_link
   
### 2. Restore the provided image files on microSD cards
   Use an open-source software called Clonezilla: https://clonezilla.org/
   Tutorial can be found: https://clonezilla.org/fine-print-live-doc.php?path=clonezilla-live/doc/03_Disk_to_disk_clone

### 3. Insert the microSD cards into a Pi cluster

