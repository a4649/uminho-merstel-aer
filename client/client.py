#! /usr/bin/python3
import socket
import sys
import os

TTL = 3
BUFFER_SIZE = 1024
IP_ADDR = '2001:0690:2280:0820:33::2'
UDP_PORT = 9999

def main(argv):
    filename = ''
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = 'file-list'

    c = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    c.settimeout(TTL)
    c.sendto(filename.encode(), (IP_ADDR, UDP_PORT))
    response, client_addr = c.recvfrom(BUFFER_SIZE)
    message = response.decode('utf8')

    if message == 'file-not-found':
        print("{} not found on server".format(filename))
        c.close()
        sys.exit(0)
    
    if 'file-list' in message:
        result = message.replace('file-list:','')
        print("Available files on server:\n{}".format(result))
        c.close()
        sys.exit(0)
        
    final = os.path.join('/home/core/file-share/client',filename)

    if os.path.exists(final):
        os.remove(final)

    if message == 'file-found':
        try:
            os.remove(final)
        except Exception:
            pass
            
    print("Downloading...")
        
    file = open(filename,'wb')

    data,addr = c.recvfrom(BUFFER_SIZE)
    try:
        while(data):
            file.write(data)
            c.settimeout(TTL)
            data, addr = c.recvfrom(BUFFER_SIZE)
    except Exception:
        file.close()
        c.close()

    file.close()
    c.close()
    
    if os.path.isfile(final):
        print(filename + " successfully downloaded!")

        
if __name__ == "__main__":
    main(sys.argv[1:])
