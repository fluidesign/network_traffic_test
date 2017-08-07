#! python3

from sys import argv, stdout
import socket
import datetime
from time import sleep

_NUMBER_OF_ARGS = 4

class Server:
    # logs when you sent the packet
    def log_data(self, timestamp, message):
        with open(self.logfile, "a") as logfile:
            logfile.write('Timestamp: ' + str(timestamp) + ', ' \
                          + 'Message: ' + str(message) + '\n')

    def open_sockets(self):
        _BUFFER_SIZE = 100
        try:
            # Create a TCP/IP socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Bind the socket to the port
            server_address = (self.local_ip, self.local_port)
            self.log_data(datetime.datetime.now(), 'starting up on {} port {}'.format(*server_address))
            sock.bind(server_address)
            # Listen for incoming connections
            sock.listen(1)
        except OSError:
            print("Error: Verify that the {port} port is not used by another process".format(port=self.local_port))
            exit()

        while True:
            # Wait for a connection
            print('waiting for a connection')
            self.log_data(datetime.datetime.now(), 'waiting for a connection on {ip}:{port}'.format(ip=self.local_ip,port=self.local_port))
            connection, client_address = sock.accept()
            try:
                print('Remote client connected from :', client_address)
                self.log_data(datetime.datetime.now(), 'connection from ' + str(client_address) + ' established...')
                self.log_data(datetime.datetime.now(), 'start communication')
                # Receive the data in small chunks and retransmit it
                while True:
                    data = connection.recv(_BUFFER_SIZE)
                    if data:
                        self.log_data(datetime.datetime.now(), 'Data: {data} received sending it back...'.format(data=data))
                        connection.sendall(data)
                    else:
                        self.log_data(datetime.datetime.now(), 'no data from ' + client_address + ' probably something wrong')
            finally:
                print("Remote client closed connection...pending for a new one")
                self.log_data(datetime.datetime.now(), "Remote client closed connection...pending for a new one")
                sock.close()
                self.open_sockets()
            sleep(1)  # Time in seconds.

    def __init__(self, argv):
        self.local_ip = argv[1]
        self.local_port = int(argv[2])
        self.logfile = argv[3]

        self.log_data(datetime.datetime.now(), '#############################')
        self.open_sockets()

def helper():
    print ("The script is expecting for {num} or argument as following:".format(num=_NUMBER_OF_ARGS-1))
    print ("{file} local_ip local_port log_file".format(file=__file__))

def main(argv):
    if (len(argv) == _NUMBER_OF_ARGS): # script name + _NUMBER_OF_ARGS
        Server(argv)
    else:
        helper()

main(argv)