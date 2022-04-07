# AER - Emergent Network Architectures curricular unit

File Sharing project usage example 

Open two linux terminals, enter folder and run scripts

Note: 
 * if you are testing directly in your virtual machine, ensure the line number 8 of the python scripts is set to the loopback interface address (::1)
 * if you are testing inside CORE, ensure the line number 8 of the python scripts is set to the server (host c1) interface address (2001:0690:2280:0820:33::2)


To start the server (host c1):

```cd /home/core/file-share/server```

```./server.py```

To download files from clients:

```cd /home/core/file-share/client```

```./client.py file1.txt```

To list files on server from client, just run the client code withou any argument:
```./client.py```

Virtual Machine image (VirtualBox):

https://uminho365-my.sharepoint.com/:u:/g/personal/pg45517_uminho_pt/EXB_Eqw--VlPmKJubNdkJ4kBWZP4DmyAXC2q7_B-MhSMow?e=eOfUTO

Note:
 * it's a fork from the image provided by University of Minho
 * automatic login (password is 'core')
 * Xubuntu
 * CORE 7.5.2
 * Visual Studio Code

Instructions: create a new virtual machine with VirtualBox, do not create disk image file, import this one


**DNS**

In order to use DNS names for ping with name of the node copy the hosts file to your CORE host:

```sudo cp Downloads/hosts /etc/hosts```
