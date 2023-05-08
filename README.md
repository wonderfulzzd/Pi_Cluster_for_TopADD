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

### 3. Insert the SD card and boot
Insert the microSD card/USB drive/external SSD drive to the Raspberry Pi. <br>
Connect internet cable, mouse and keyboard, monitor. <br>
Connect power supply and boot.

### 4. Setup the OS

#### 4.1 Internet connection
wifi
> sudo nano /etc/netplan/01-network-manager-all.yaml

Type the following into the file:
```
# Let NetworkManager manage all devices on this system
 network:
  version: 2
  renderer: NetworkManager
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
> sudo netplan generate
> sudo netplan apply

Wifi should have been connected.

#### 4.2 Enable SSH
Install OpenSSH server program:
> sudo apt install openssh-server 
Check the status of the ssh server:
> sudo systemctl status ssh
Use the UFW (Uncomplicated FireWall) to allow SSH connections:
> sudo ufw allow ssh


#### 4.3 Enable screen sharing
Connect a laptop to the switch <br>
<img src="https://user-images.githubusercontent.com/19493039/236723444-743861a7-bd64-4de4-8e89-32581a72d0b0.png" width=50% height=50%>
<img src="https://user-images.githubusercontent.com/19493039/236728172-8e493577-d68f-4e60-b645-2ea88bf02a1d.png" width=50% height=50%>



https://glmdev.medium.com/building-a-raspberry-pi-cluster-784f0df9afbd <br>

#### 4.2 MPICH
> sudo apt install mpich

#### 4.3 PETSc
On the NAS directory from step 3.1, called "clusterfs", install the software PETSc. <br>
The official instruction: <br>
https://petsc.org/main/install/install/ <br>
The configuration I used: <br>
> ./configure PETSC_DIR=/clusterfs/opt/petsc-3.10.2 PETSC_ARCH=arch-linux-mpicc-release --COPTFLAGS='-O3' --CXXOPTFLAGS='-O3' --FOPTFLAGS='-O3' --with-hypre-dir=/clusterfs/opt/hypre-2.14.0 --with-debugging=0 --with-cc=mpicc --with-cxx=mpicxx --with-fc=mpif90  <br>
       
### 5. Clone multiple microSD
Use an open-source software called Clonezilla: https://clonezilla.org/
Tutorial can be found: https://clonezilla.org/fine-print-live-doc.php?path=clonezilla-live/doc/03_Disk_to_disk_clone
    
4. Mu
5. d
6. d


## Method 2: Restore from the provided image files
### 1. Download the provided image files
   https://drive.google.com/drive/folders/1AKukyrJqC8yL2S2H1plEN8ZqoN_B8zXJ?usp=share_link
   
### 2. Restore the provided image files on microSD cards
   Use an open-source software called Clonezilla: https://clonezilla.org/
   Tutorial can be found: https://clonezilla.org/fine-print-live-doc.php?path=clonezilla-live/doc/03_Disk_to_disk_clone

### 3. Insert the microSD cards into a Pi cluster

