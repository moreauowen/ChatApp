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


class User:
    """
    The User class represents a unique user.
    This class is used to store all user-related info including the socket to be accessed easily.
    """
    def __init__(self):
        self.user_name = input("Please enter your display name: ")
        self.dest_addr = input("Enter the address of the server you'd like to reach: ")
        self.dest_port = input("Enter the port of the server you'd like to reach: ")

        self.user_address = socket.gethostbyname(socket.gethostname())
        self.user_socket = create_socket()

        self.connected = False

    def new_connection(self):
        try:
            self.user_socket.connect(self.dest_addr, self.dest_port)
        except socket.gaierror as err1:
            print("Oops! Error while connecting to server. Restart program and try again.")
            print("Error: {}".format(err1))
            sys.exit(1)
        except socket.error as err2:
            print("Oops! Error with client socket. Restart program and try again.")
            print("Error: {}".format(err2))
            sys.exit(1)
        print("[INFO]: Now connected to {}:{}!".format(self.dest_addr, self.dest_port))
        self.connected = True

    def send_message(self):
        try:
            new_message = input(" -> ")
            self.user_socket.send(new_message.encode())
        except socket.error as err:
            print("Oops! Error while sending message. Please restart program and try again.")
            print("Error: {}".format(err))
            sys.exit(1)

    def recv_message(self):
        try:
            server_response = self.user_socket.recv(1024).decode()
            #if server_response == "1":
                # Message wasn't received properly
            #elif server_response == "0":
                # Message properly received
        except socket.error as err:
            print("Oops! Error while receiving response. Please restart program and try again.")
            print("Error: {}".format(err))
            sys.exit(1)


def create_socket():
    try:
        new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return new_socket
    except socket.error as err:
        print("Oops! Error while creating socket. Please restart program and try again.")
        print("Error: {}".format(err))
        sys.exit(1)


def run_client():
    client = User()
    client.new_connection()
    print(client)
    print("Test test")


if __name__ == "__main__":
    run_client()