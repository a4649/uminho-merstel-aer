# AER
Emergent Network Architectures

File Sharing project usage example

Open two linux terminals, enter folder and run scripts

Note: 
 * if you are testing directly in your virtual machine, ensure the line number 8 of the pythons scripts is set to the loopback interface address (::1)
 * if you are testing inside CORE, ensure the line number 8 of the pythons scripts is set to the server interface address (2001:680:2280:21::2)


To start the server:

```cd /home/core/file-share/server```

```./server.py```

To download files from clients:

```cd /home/core/file-share/client```

```./client.py example1.txt```
