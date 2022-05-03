#! /usr/bin/python3
from asyncore import file_dispatcher
import socket
import os
import sys
import threading

TTL = 5
#IP_ADDR = '2001:0690:2280:0820:33::2'
IP_ADDR = '::1'
UDP_PORT = 9999
BUFFER_SIZE = 1024
FILES_FOLDER = '/home/core/file-share/server/files'

def get_files():
    file_dict = {}
    file_list = os.listdir(FILES_FOLDER)
    for file in file_list:
        file_dict[file] = os.path.getsize(os.path.join(FILES_FOLDER,file))
    return "file-list:\n{}".format(file_dict)

def handle_client(file_name, client_addr):
    """ Check if requested file exists and send it to client
    Args:
        connect: socket
        file_name: requested file
        client_addr: tupple with (ip,port)
    """
    connection = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    if file_name.decode('utf-8') == 'file-list':
        list_of_files = get_files()
        print('Sending list fo files:\n {}'.format(list_of_files))
        connection.sendto(list_of_files.encode(), client_addr)
        return

    file_path = os.path.join(FILES_FOLDER, file_name.decode('utf-8'))
    if not os.path.isfile(file_path):
        print("{} not found".format(file_path))
        connection.sendto("file-not-found".encode(), client_addr)
        return
    else:
        connection.sendto("file-found".encode(), client_addr)

    file = open(file_path,'rb')
    data = file.read(BUFFER_SIZE)
    while data:
        if(connection.sendto(data, client_addr)):
            print("Sending {} to {}...".format(file_path,client_addr[0]))
            data = file.read(BUFFER_SIZE)
    file.close()
    print("Done!")

def main():
    try:
        s = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        s.bind((IP_ADDR, UDP_PORT))
        print("Accepting clients on {}:{}...".format(IP_ADDR, UDP_PORT))
        print("Press Ctrl+C to terminate")
        # s.setblocking(0)
        # s.settimeout(15)
    except socket.error:
        print("Failed to bind on {}:{}...".format(IP_ADDR, UDP_PORT))
        sys.exit(1)

    while True:
        try:
            request, client_addr = s.recvfrom(BUFFER_SIZE)
            print(request.decode('utf8'))
            threading.Thread(target=handle_client(request,client_addr)).start()
        except KeyboardInterrupt:
            s.close()
            sys.exit(0)


if __name__ == "__main__":
    main()
