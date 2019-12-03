"""
Client program for multi-threaded TCP Chat Application.
Final Project - Network Programming, Fall 2019
Professor Salem Othman
Fri, Oct 25, 2019

:authors:
    Owen Moreau, Jian Huang, Mario La
"""
import socket
import sys
import select
from _thread import *

# TODO - Remove following after testing
# The following are hard-coded in temporarily for local testing
DEV_SERVER_ADDR = "169.254.128.210"
DEV_SERVER_PORT = 5000


class User:
    """
    The User class represents a unique user.
    This class is used to store all user-related info including the socket to be accessed easily.

    NOTE - We would like to send the User object information over with each message but we are simply sending
           the encoded string message until base functionality is complete.
    """
    def __init__(self):
        self.user_name = input("Enter your display name: ")
        # self.dest_addr = input("Enter the DESTINATION ADDRESS of the server: ")
        self.dest_addr = DEV_SERVER_ADDR
        # self.dest_port = input("Enter the DESTINATION PORT of the server: ")
        self.dest_port = DEV_SERVER_PORT

        self.user_address = socket.gethostbyname(socket.gethostname())
        self.user_socket = create_socket()

    def __str__(self):
        display = "Name: {}, IP: {}".format(self.user_name, self.user_address)
        return display

    def new_connection(self):
        """
        Establishes a new connection to socket at User's destination address and port.
        """
        try:
            # Creates destination tuple including entered destination address and port
            destination = (self.dest_addr, int(self.dest_port))
            self.user_socket.connect(destination)
        except socket.gaierror as err1:
            print("[FATAL] Oops! Error while connecting to server. Restart program and try again.")
            print("Error: {}".format(err1))
            sys.exit(1)
        except socket.error as err2:
            print("[FATAL] Oops! Error with client socket. Restart program and try again.")
            print("Error: {}".format(err2))
            sys.exit(1)
        print("[INFO]: Now connected to {}:{}!".format(self.dest_addr, self.dest_port))
        print("________________________________________________________________________________________")

    def send_message(self, msg):
        """
        Sends encoded message through socket.
        :param msg: Message that the user entered
        """
        try:
            new_message = msg
            self.user_socket.send(new_message.encode())
        except socket.error as err:
            print("[FATAL] Oops! Error while sending message. Please restart program and try again.")
            print("Error: {}".format(err))
            sys.exit(1)

    def receive_message(self):
        """
        Receives response message from server and decodes it.
        :return: Received message
        """
        try:
            server_response = self.user_socket.recv(1024).decode()
            return server_response
        except socket.error as err:
            print("[FATAL] Oops! Error while receiving response. Please restart program and try again.")
            print("Error: {}".format(err))
            sys.exit(1)


def create_socket():
    """
    Creates a new TCP socket to connect to server socket.
    """
    try:
        new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return new_socket
    except socket.error as err:
        print("[FATAL] Oops! Error while creating socket. Please restart program and try again.")
        print("Error: {}".format(err))
        sys.exit(1)


def check_for_end(message):
    """
    Helper function to determine if message is to STOP connection or not.
    :param message: given message
    :return: True if message stops program, else False
    """
    if message == "STOP":
        return True
    else:
        return False


def print_thread(sock):
    print()


def run_client():
    """
    Rough draft of client program still in development.
    TODO - Add better documentation once functionality complete.
    """
    print("_____________________CHAT APPLICATION v0.1.0 (CLIENT_DEV)_____________________")
    client = User()
    client.new_connection()

    running = True
    while running:
        socket_list = [client.user_socket]
        read_sockets, w, e = select.select(socket_list, [], [])

        # Must add sys.stdin to loop because select() only works with sockets in Windows
        # Not any file descriptor like Linux
        for sock in read_sockets + [sys.stdin]:
            if sock == client.user_socket:
                response = client.receive_message()
                if check_for_end(response):
                    running = False
                print(response)
            else:
                new_msg = sys.stdin.readline()
                client.send_message(new_msg)
                if check_for_end(new_msg):
                    running = False
                # sys.stdout.write("[YOU]: ")
                # sys.stdout.write(new_msg)
                sys.stdout.flush()

    client.user_socket.close()
    print("[INFO] The connection was successfully closed. Thanks for using ChatApp!")


if __name__ == "__main__":
    run_client()
