# AER - Emergent Network Architectures curricular unit

File Sharing project usage example 

Open two linux terminals, enter folder and run scripts

Note: 
 * if you are testing directly in your virtual machine, ensure the line number 8 of the python scripts is set to the loopback interface address (::1)
 * if you are testing inside CORE, ensure the line number 8 of the python scripts is set to the server interface address (2001:680:2280:21::2)


To start the server:

```cd /home/core/file-share/server```

```./server.py```

To download files from clients:

```cd /home/core/file-share/client```

```./client.py file1.txt```

Virtual Machine image (VirtualBox):

https://uminho365-my.sharepoint.com/:u:/g/personal/pg45517_uminho_pt/EXB_Eqw--VlPmKJubNdkJ4kBWZP4DmyAXC2q7_B-MhSMow?e=eOfUTO

Note:
 * it's a fork from the image provided by University of Minho
 * automatic login (password is 'core')
 * Xubuntu
 * CORE 7.5.2
 * Visual Studio Code

Instructions: create a new virtual machine with VirtualBox, do not create disk image file, import this one
