import socket
import sys
import os

TTL = 3
BUFFER_SIZE = 1024
IP_ADDR = '::1'
UDP_PORT = 9999

def main(argv):
    print("hello")
    filename = sys.argv[1]

    c = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    c.settimeout(TTL)
    c.sendto(filename.encode(), (IP_ADDR, UDP_PORT))
    response, client_addr = c.recvfrom(BUFFER_SIZE)
    message = response.decode('utf8')

    if message == 'file-not-found':
        print("{} not found on server".format(filename))
        c.close()
        sys.exit(0)

    if os.path.exists(filename):
        os.remove(filename)

    if message == 'file-found':
        print("Downloading...")
        
    file = open(filename,'wb')

    data,addr = c.recvfrom(BUFFER_SIZE)
    try:
        while(data):
            file.write(data)
            c.settimeout(TTL)
            data, addr = c.recvfrom(BUFFER_SIZE)
    except:
        file.close()
        c.close()

    print("Successfully downloaded!")

if __name__ == "__main__":
    main(sys.argv[1:])
