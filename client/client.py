#! /usr/bin/python3
import socket
import sys
import os
import hashlib
import time

TTL = 5
BUFFER_SIZE = 2048
#IP_ADDR = '2001:0690:2280:0820:33::2'
IP_ADDR = '::1'
UDP_CONTROL_PORT = 9999

client_socket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)

file_blocks_array = []

def check_checksums(hash_a, hash_b):
    return hash_a == hash_b

def get_block_info(file, block_number):
    try:
        client_socket.sendto(('block-info:' + file + ':' + block_number).encode(),(IP_ADDR, UDP_CONTROL_PORT))
        response, server_addr = client_socket.recvfrom(BUFFER_SIZE)
        return response
    except socket.timeout as err:
        print("Get timeout, tryng again in {} seconds...".format(TTL))
        time.sleep(TTL)
        return get_block_info(file, block_number)
    except IOError as err:
        if err.errno == 101:
            print("Network is unreachable, trying again in {} seconds...".format(TTL))
            time.sleep(TTL)
            return get_block_info(file, block_number)

def download_block(file, block_number):
    try:
        print('REQUESTING BLOCK {}'.format(block_number))
        client_socket.sendto(('file-data:' + file + ':' + str(block_number)).encode(),(IP_ADDR, UDP_CONTROL_PORT))
        response, server_addr = client_socket.recvfrom(BUFFER_SIZE)
        return response
    except socket.timeout as err:
        print("Get timeout, tryng again in {} seconds...".format(TTL))
        time.sleep(TTL)
        return download_block(file, block_number)
    except IOError as err:
        if err.errno == 101:
            print("Network is unreachable, trying again in {} seconds...".format(TTL))
            time.sleep(TTL)
            return download_block(file, block_number)


def get_checksum(bdata):
    return hashlib.md5(bdata).hexdigest()

def check_block(block):
    if block is None:
        return False
    rec_file = block.split(';'.encode())[0].decode('utf-8')
    rec_block = block.split(';'.encode())[1].decode('utf-8')
    tmp = block.replace(block.split(';'.encode())[0]+';'.encode(),''.encode())
    rec_bdata = tmp.replace(block.split(';'.encode())[1] +';'.encode(),''.encode())

    block_info = get_block_info(rec_file, rec_block)

    block_info_file = block_info.split(':'.encode())[1].decode('utf-8')
    block_info_block_num = block_info.split(':'.encode())[2].decode('utf-8')
    block_info_checksum = block_info.split(':'.encode())[3].decode('utf-8')

    if ((block_info_file == rec_file) and (block_info_block_num == rec_block) and (block_info_checksum == get_checksum(rec_bdata))):
        return True

    return False

def get_file(file, blocks):
    num_blocks = int(blocks)
    
    for i in range(num_blocks):
        # download single block
        tmp_block = download_block(file, i)
        x = 0
        # check if block (md5 checksum is correct, if not, download again, in loop)
        while x < 1:
            if check_block(tmp_block):
                print("Block {} is correct!".format(tmp_block.split(';'.encode())[1].decode('utf-8')))
                tmp = tmp_block.replace(tmp_block.split(';'.encode())[0]+';'.encode(),''.encode())
                rec_bdata = tmp.replace(tmp_block.split(';'.encode())[1] +';'.encode(),''.encode())
                file_blocks_array.insert(i, rec_bdata)
                x = 2
            else:
                print("Block {} is invalid!".format(tmp_block.split(';'.encode())[1].decode('utf-8')))

    try:
        os.remove(file)
    except Exception:
        pass

    # write file on disk
    local_file = open(file,'wb')
    for i in file_blocks_array:
        try:
            local_file.write(i)
        except Exception:
            local_file.close()
    local_file.close()
    print("Download complete!")
    sys.exit(0)

def main(argv):
    request = ''
    try:
        request = 'file-info:' + sys.argv[1]
    except IndexError:
        request = 'file-list'

    client_socket.settimeout(TTL)
    client_socket.sendto(request.encode(), (IP_ADDR, UDP_CONTROL_PORT))
    response, server_addr = client_socket.recvfrom(BUFFER_SIZE)
    message = response.decode('utf8')

    if message == 'file-not-found':
        print("{} not found on server".format(sys.argv[1]))
        client_socket.close()
        sys.exit(0)

    if 'file-list' in message:
        result = message.replace('file-list:','')
        print("Available files on server:\n{}".format(result))
        client_socket.close()
        sys.exit(0)

    if 'file-info' in message:
        tmp_file = message.split(':')[1]
        tmp_file_blocks = message.split(':')[2]
        get_file(tmp_file, tmp_file_blocks)

        
if __name__ == "__main__":
    main(sys.argv[1:])
