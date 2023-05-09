# Pi_Cluster_for_TopADD
A Raspberry Pi cluster for the TopADD program

The following discussion on configurations assumes one has physically built a Raspberry Pi cluster, for example: <br>
<img src="https://user-images.githubusercontent.com/19493039/236486047-83bff4b4-61f6-40b2-8cef-3ce520924f31.png" width=50% height=50%> <br>

The above cluster consists of 5 nodes, including 1 login node (in the black case) and 4 computing node.

## Method 1: Fresh installation

### 1. Download Raspberry Pi imager
https://downloads.raspberrypi.org/imager/imager_latest.exe <br>
   
   
### 2. Flash the SDs
Use Raspberry Pi imager to install OS on microSD <br>
https://www.youtube.com/watch?v=ntaXWS8Lk34 <br>
<img src="https://user-images.githubusercontent.com/19493039/236950684-e8c50b4f-6f36-4516-915d-f12aaea5950a.png" width=50% height=50%> <br>


### 3. Insert the SD card and boot
Insert the microSD card/USB drive/external SSD drive to the Raspberry Pi. <br>
Connect internet cable, mouse and keyboard, monitor. <br>
Connect power supply and boot. <br>


### 4. Setup the OS

#### 4.1 Login
For Ubuntu 22.04, the default user name and password are both 'ubuntu' if you did not create a user name and password in the Advanced options menu when flashing the SD card. <br>
You will be asked to change password immediately after you login. You may change the password to 'raspberry'. <br>

#### 4.2 Change hostname
Check the hostname by:
> hostname <br>

You may want to change the hostname. <br>

Change the hostname permanently
> sudo hostnamectl set-hostname rpi0 <br>

#### 4.3 Enable SSH
For Ubuntu 22.04, the SSH seems to be enabled by default.

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


You may want to change the hosts, which will be the ip and hostname for the other nodes in the cluster. The hosts can be changed as follows:
> sudo nano /etc/hosts <br>

#### 4.5 Change hosts
Hosts are the hosts ip and names for your other nodes in the cluster. You can check them in /etc/hosts. <br>
> sudo /etc/hosts <br>

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
#### 4.6 Update OS
> sudo apt-get update <br>

#### 4.7 Install make 
"make" is used to build groups of programs from the source code.
> sudo apt-get install make <br>

#### 4.8 MPICH
> sudo apt-get install mpich <br>

#### 4.9 Install hypre
Download hypre
> wget -c https://github.com/hypre-space/hypre/archive/refs/tags/v2.19.0.tar.gz <br>

Install hypre
> tar -xof v2.19.0.tar.gz <br>
> cd hypre-2.19.0/src <br>
> ./configure --prefix=/home/ubuntu/opt --enable-shared <br>
> make -j4 install <br>

#### 4.10 Install libblas liblapack
Lapack is a standard software library for numerical linear algebra. It relies on BLAS implementation.
Install
> sudo apt-get install libblas-dev liblapack-dev <br>

#### 4.11 Install hypre
> tar -xof v2.19.0.tar.gz <br>
> cd hypre-2.19.0/src <br>
> ./configure --prefix=/home/ubuntu/opt --enable-shared <br>
> make -j4 install <br>

#### 4.12 Install PETSc
The official instruction: <br>
https://petsc.org/main/install/install/ <br>

Download PETSc
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
Change the IP address
> sudo nano /etc/netplan/01-network-manager-all.yaml <br>

For example: <br>
192.168.137.161 for rpi1 <br>
192.168.137.162 for rpi2 <br>
192.168.137.163 for rpi3 <br>
192.168.137.164 for rpi4 <br>


### 7. Set up password-less SSH login
Enable to login to a remote computer via ssh without having to enter the password
Go to .ssh directory
> cd ~/.ssh <br>
Generate a SSH key
> ssh-keygen <br>
Copy the key to remote desktop, e.g rpi1,
> ssh-copy-id ubuntu@rpi1 <br>
Test the setup whether is successful
> ssh ubuntu@rpi1 <br>


### 8. Try run the TopADD program
Clone the TopADD repo on github
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

### 9. (optional) Network file system (NFS)
A shared storage is needed on a cluster when each node needs to be able to access the same files. This can be achieved by setting up a net
If Ubuntu desktop is installed on a Raspberry Pi, then the Pi can be remotelly controlled. <br>
<img src="https://user-images.githubusercontent.com/19493039/236723444-743861a7-bd64-4de4-8e89-32581a72d0b0.png" width=80% height=80%> <br>
<img src="https://user-images.githubusercontent.com/19493039/236728172-8e493577-d68f-4e60-b645-2ea88bf02a1d.png" width=80% height=80%> <br>

Install TightVNC Viewer on a Windows laptop/desktop. Connect the laptop to the switch connecting the Pi.
<img src="https://user-images.githubusercontent.com/19493039/237030336-ff45598e-e2f2-4481-aa05-497b94137b35.png" width=50% height=50%> <br>

Reference: <br>
https://glmdev.medium.com/building-a-raspberry-pi-cluster-784f0df9afbd

### 10. (optional) Enable screen sharing
If Ubuntu desktop is installed on a Raspberry Pi, then the Pi can be remotelly controlled. <br>
<img src="https://user-images.githubusercontent.com/19493039/236723444-743861a7-bd64-4de4-8e89-32581a72d0b0.png" width=80% height=80%> <br>
<img src="https://user-images.githubusercontent.com/19493039/236728172-8e493577-d68f-4e60-b645-2ea88bf02a1d.png" width=80% height=80%> <br>

Install TightVNC Viewer on a Windows laptop/desktop. Connect the laptop to the switch connecting the Pi.
<img src="https://user-images.githubusercontent.com/19493039/237030336-ff45598e-e2f2-4481-aa05-497b94137b35.png" width=50% height=50%> <br>



## Method 2: Restore from the provided image files
### 1. Download the provided image files
   https://drive.google.com/drive/folders/1AKukyrJqC8yL2S2H1plEN8ZqoN_B8zXJ?usp=share_link
   
### 2. Restore the provided image files on microSD cards
   Use an open-source software called Clonezilla: https://clonezilla.org/
   Tutorial can be found: https://clonezilla.org/fine-print-live-doc.php?path=clonezilla-live/doc/03_Disk_to_disk_clone

### 3. Insert the microSD cards into a Pi cluster

