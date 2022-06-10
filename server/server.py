#! /usr/bin/python3
from asyncore import file_dispatcher
import socket
import os
import sys
import threading
import math
import hashlib

TTL = 5
#IP_ADDR = '2001:0690:2280:0820:33::2'
IP_ADDR = '::1'
UDP_CONTROL_PORT = 9999
UDP_DATA_PORT = 9991
BUFFER_SIZE = 2048
BLOCK_SIZE = 1984
FILES_FOLDER = '/home/core/file-share/server/files'

control_socket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
data_socket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)

def get_checksum(bdata):
    return hashlib.md5(bdata).hexdigest()

def get_files():
    file_dict = {}
    file_list = os.listdir(FILES_FOLDER)
    for file in file_list:
        file_dict[file] = os.path.getsize(os.path.join(FILES_FOLDER,file))
    return "file-list:\n{}".format(file_dict)

def get_file_size(file):
    return os.path.getsize(file)

def send_data(data, addr):
    tmp_socket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    tmp_socket.sendto(data.encode(), addr)

def check_file(file):
    if not 'home' in file:
        file = os.path.join(FILES_FOLDER,file)
    return os.path.isfile(os.path.join(FILES_FOLDER, file))

def send_file_info(file, addr):
    if not check_file(file):
        send_data("file-not-found", addr)
        sys.exit()
    tmp_file = os.path.join(FILES_FOLDER,file)
    #print("Getting info for file: " + tmp_file)
    size_of_file = get_file_size(tmp_file)
    tmp_seq = size_of_file / BLOCK_SIZE
    blocks = math.ceil(tmp_seq)
    lista = []
    file_dict ={}
    tmp_file = open(tmp_file,'rb')
    for i in range(blocks):
        tmp_data = tmp_file.read(BLOCK_SIZE)
        lista.append(tmp_data)
        file_dict[i] = get_checksum(tmp_data)
    tmp_file.close()
    tmp_response = 'file-info:' + file + ':' + str(len(file_dict))
    #tmp_response = 'file-info:' + file + ':' + str(len(lista))
    print('REPLY: {}'.format(tmp_response))
    tmp_socket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    tmp_socket.sendto(tmp_response.encode(), addr) 

def send_block_info(file, block, addr):
    if not check_file(file):
        send_data("file-not-found", addr)
        sys.exit()
    tmp_file = os.path.join(FILES_FOLDER,file)
    size_of_file = get_file_size(tmp_file)
    tmp_seq = size_of_file / BLOCK_SIZE
    blocks = math.ceil(tmp_seq)
    file_dict ={}
    tmp_file = open(tmp_file,'rb')
    for i in range(blocks):
        tmp_data = tmp_file.read(BLOCK_SIZE)
        file_dict[i] = get_checksum(tmp_data)
    tmp_file.close()

    if int(block) < len(file_dict):
        tmp_response = 'block-info:' + file + ':' + block + ':' + file_dict[int(block)]
        print('REPLY: {}'.format(tmp_response))
        tmp_socket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        tmp_socket.sendto(tmp_response.encode(), addr)
    else:
        tmp_socket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        tmp_socket.sendto("Invalid block number".encode(), addr)

def send_data_block(file, seq, addr):
    if not check_file(file):
        send_data("file-not-found", addr)
        sys.exit()
    #print("Sending {} block number {}".format(file, seq))
    tmp_socket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    tmp_file = os.path.join(FILES_FOLDER,file)
    size_of_file = get_file_size(tmp_file)
    tmp_seq = size_of_file / BLOCK_SIZE
    blocks = math.ceil(tmp_seq)
    lista = []
    read_file = open(tmp_file,'rb')
    for i in range(blocks):
        lista.append(read_file.read(BLOCK_SIZE))
    read_file.close()
    tmp_header = (file + ';' + seq + ';')
    #print('TOTAL BLOCOS:{}'.format(len(lista)))
    #print('REPLY: {}{}'.format(tmp_header, lista[int(seq)]))
    print('REPLY: {}{}'.format(tmp_header, "***binary data***"))
    x = tmp_socket.sendto(tmp_header.encode() + lista[int(seq)], addr)
    print("SENT: {} bytes".format(x))

def handle_client(request, client_addr):
    """ Check if requested file exists and send it to client
    Args:
        connect: socket
        file_name: requested file
        client_addr: tupple with (ip,port)
    """
    tmp_socket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    tmp_request = request.decode('utf-8')

    # handle list of available files request
    if  tmp_request == 'file-list':
        list_of_files = get_files()
        print('REPLY: {}'.format(list_of_files))
        tmp_socket.sendto(list_of_files.encode(), client_addr)
        return

    # handle file info request
    if 'file-info' in tmp_request:
        tmp_file = tmp_request.split(':')[1]
        send_file_info(tmp_file, client_addr)
        return
        
    # handle file block request
    if 'file-data' in tmp_request:
        tmp_file = tmp_request.split(':')[1]
        tmp_block = tmp_request.split(':')[2]
        send_data_block(tmp_file, tmp_block,client_addr)
        return

    if 'block-info' in tmp_request:
        tmp_file = tmp_request.split(':')[1]
        tmp_block = tmp_request.split(':')[2]
        send_block_info(tmp_file, tmp_block,client_addr)
        return
 
    # invalid request, kill thread
    send_data('Invalid request', client_addr)
    return
        
def main():
    try:
        control_socket.bind((IP_ADDR, UDP_CONTROL_PORT))
        data_socket.bind((IP_ADDR, UDP_DATA_PORT))
        print("Accepting clients on {}:{}...".format(IP_ADDR, UDP_CONTROL_PORT))
        print("Press Ctrl+C to terminate")
    except socket.error:
        print("Failed to bind on {}:{}...".format(IP_ADDR, UDP_CONTROL_PORT))
        sys.exit(1)

    while True:
        try:
            request, client_addr = control_socket.recvfrom(BUFFER_SIZE)
            print('REQUEST: {}'.format(request.decode('utf8')))
            threading.Thread(target=handle_client(request,client_addr)).start()
        except KeyboardInterrupt:
            control_socket.close()
            data_socket.close()
            sys.exit(0)


if __name__ == "__main__":
    main()
