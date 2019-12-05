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
import time
from _thread import *


class User:
    """
    The User class represents a unique user.
    This class is used to store all user-related info including the socket to be accessed easily.

    NOTE - We would like to send the User object information over with each message but we are simply sending
           the encoded string message until base functionality is complete.
    """
    def __init__(self):
        self.dest_addr = input("Enter the DESTINATION ADDRESS of the server: ")
        self.dest_port = input("Enter the DESTINATION PORT of the server: ")

        self.user_address = socket.gethostbyname(socket.gethostname())
        self.user_socket = create_socket()

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


def recv_msg_thread(client):
    """
    Client's thread process for receiving and printing messages. If message is simply "OK" response
    then it is not printed.
    :param client: User object for connected client
    """
    running = True
    while running:
        message = client.receive_message()
        if message != "OK":
            print(message)
        elif check_for_end(message):
            running = False

    client.user_socket.close()


def send_msg_thread(client):
    """
    Client's thread process for typing and sending messages.
    :param client:
    :return:
    """
    running = True
    while running:
        new_msg = sys.stdin.readline()
        client.send_message(new_msg)
        print("\n[YOU]: {}".format(new_msg))
        if check_for_end(new_msg):
            running = False

    client.user_socket.close()


def run_client():
    """
    Client program builds a new User object and establishes connection.
    A thread process starts for receiving/printing messages as well as typing/sending messages.
    """
    print("__________________________CHAT APPLICATION v0.1.0__________________________")
    client = User()
    client.new_connection()

    while True:
        time.sleep(1)
        start_new_thread(recv_msg_thread, (client,))
        start_new_thread(send_msg_thread, (client,))


if __name__ == "__main__":
    run_client()
