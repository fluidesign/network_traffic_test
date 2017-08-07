from sys import argv, stdout
from time import sleep
import socket
import datetime

_NUMBER_OF_ARGS = 4

class Client:
    # logs when you sent the packet
    def log_data(self, timestamp, message):
        with open(self.logfile, "a") as logfile:
            logfile.write('Timestamp: ' + str(timestamp) + ', ' \
                          + 'Message: ' + str(message) + '\n')


    def open_sockets(self):
        _RETRY_IN_SECONDS = 2
        _BUFFER_SIZE = 100
        try:
            # Create a TCP/IP socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Connect the socket to the port where the server is listening
            server_address = (self.server_ip, self.server_port)
            print('connecting to {} port {}'.format(*server_address))
            self.log_data(datetime.datetime.now(), 'connecting to {} port {}'.format(*server_address))
            sock.connect(server_address)
        except ConnectionRefusedError:
            print ("Connection refused, verify the server is listen on the right port and its accessible")
            print('Will retry again in {retry} seconds'.format(retry=_RETRY_IN_SECONDS))
            sleep(_RETRY_IN_SECONDS)
            self.open_sockets()

        self.log_data(datetime.datetime.now(), 'Connected...starting communication with remote server...')
        while True:
            try:
                # Send data
                message = b'Message in the bottle...'
                sock.sendall(message)
                # Look for the response
                amount_received = 0
                amount_expected = len(message)
                while amount_received < amount_expected:
                    data = sock.recv(_BUFFER_SIZE)
                    amount_received += len(data)
                self.log_data(datetime.datetime.now(), 'Data: {data} sent and received successfully, continue...'.format(data=data))
                sleep(1)  # Time in seconds.
            except ConnectionError:
                print('Server is not responding, trying again in {retry}'.format(retry=_RETRY_IN_SECONDS))
                self.log_data(datetime.datetime.now(), 'Server is not responding, trying again in {retry}'.format(retry=_RETRY_IN_SECONDS))
                sleep(_RETRY_IN_SECONDS)
                self.open_sockets()

    def __init__(self, argv):
        self.server_ip = argv[1]
        self.server_port = int(argv[2])
        self.logfile = argv[3]

        self.log_data(datetime.datetime.now(), '#############################')
        self.open_sockets()


def helper():
    print ("The script is expecting for {num} or argument as following:".format(num=_NUMBER_OF_ARGS-1))
    print ("{file} remote_ip remote_port log_file".format(file=__file__))


def main(argv):
    if (len(argv) == _NUMBER_OF_ARGS): # script name + _NUMBER_OF_ARGS
        Client(argv)
    else:
        helper()


main(argv)