# Emergent Network Architectures

Project developed during the Emergent Network Architectures curricular unit of the Engineering of Computer Networks and Telematic Services from School of Engineering, University of Minho https://www.eng.uminho.pt/en/study/_layouts/15/UMinho.PortaisUOEI.UI/Pages/CatalogoCursoDetail.aspx?itemId=3929&catId=12

This project aims to develop an network application that must support mobility among the nodes of the network. To achieve the goal the work is divided into three main parts. The first one is to create the infra-structured network and integrate it with the nodes that are able to move - acting as an ad-hoc. Then, the application is developed, in our case, it is a file transfer application where nodes with mobility must be able to access and download files from the server in the infra-structured network. The last goal is to develop a DTN module that gives the nodes the capability to store and forward the packets, acting as a router and improving the network’s
performance.


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


**DNS**

In order to use DNS names for ping with name of the node copy the hosts file to your CORE host:

```sudo cp Downloads/hosts /etc/hosts```

**Movement Generator**

Run the python code
Copy the output and paste it in .scen file

RFC 783 - TFTP Protocol (revision 2): 
https://datatracker.ietf.org/doc/html/rfc783
