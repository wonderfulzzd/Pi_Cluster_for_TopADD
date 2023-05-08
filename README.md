# Pi_Cluster_for_TopADD
A Raspberry Pi cluster for the TopADD program

**Method 1: Fresh installation**
1. Download Raspberry Pi imager
   https://downloads.raspberrypi.org/imager/imager_latest.exe
   
2. Flash the SDs
   Use Raspberry Pi imager to install OS on microSD
   https://www.youtube.com/watch?v=ntaXWS8Lk34
   ![image](https://user-images.githubusercontent.com/19493039/236716118-559bbcb7-0bce-4ec0-99e0-819e191e2d1e.png)

   
3. Setup the OS
   3.1 Basic setups
       https://glmdev.medium.com/building-a-raspberry-pi-cluster-784f0df9afbd
   3.2 MPICH
       sudo apt install mpich
   3.3 PETSc
       On the NAS directory from 3.1, called "clusterfs", install PETSc.
       The official instruction: https://petsc.org/main/install/install/
       The configuration I used:
       
       
       
   

4. Clone multiple microSD
   Use an open-source software called Clonezilla: https://clonezilla.org/
   Tutorial can be found: https://clonezilla.org/fine-print-live-doc.php?path=clonezilla-live/doc/03_Disk_to_disk_clone
    
4. Mu
5. d
6. d


**Method 2: Restore from the provided image files**
1. Download the provided image files
   https://drive.google.com/drive/folders/1AKukyrJqC8yL2S2H1plEN8ZqoN_B8zXJ?usp=share_link
   
2. Restore the provided image files on microSD cards
   Use an open-source software called Clonezilla: https://clonezilla.org/
   Tutorial can be found: https://clonezilla.org/fine-print-live-doc.php?path=clonezilla-live/doc/03_Disk_to_disk_clone

3. Insert the microSD cards into a Pi cluster

![IMG_9248](https://user-images.githubusercontent.com/19493039/236486047-83bff4b4-61f6-40b2-8cef-3ce520924f31.png)
