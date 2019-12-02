"""
Multi-threaded TCP Server for Chat Application.
Final Project - Network Programming, Fall 2019
Professor Salem Othman
Fri, Oct 25, 2019

:authors:
    Owen Moreau, Jian Huang, Mario La
"""
import socket
from _thread import *

client_list = []


# cd "Documents\School Related\Sophomore Year 2019-2020\Network Programming\Final\ChatApp"
class ThreadedServer:
    """
    ThreadedServer class represents threaded server for TCP Chat Application.
    """
    def __init__(self):
        self.server_addr = socket.gethostbyname(socket.gethostname())
        self.server_port = 5000
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.server_addr, self.server_port))
        self.server_socket.listen(10)
        self.print_startup_msg()

    def __str__(self):
        print_server = "  CHAT APPLICATION v0.1.0 | Address: {}, Port: {}".format(self.server_addr, self.server_port)
        return print_server

    def accept_connection(self):
        """
        Wrapper function to add new connection to client_list and print to console.
        :return: connection_socket, addr
        """
        connection_socket, addr = self.server_socket.accept()
        client_list.append(connection_socket)
        print("[INFO]: Client connected from {}:{}!".format(str(addr[0]), str(addr[1])))
        return connection_socket, addr

    def print_startup_msg(self):
        print("________________________________________________________________________________________")
        print(self)
        print("________________________________________________________________________________________")


def client_thread(conn_socket, addr):
    """
    TODO - UPDATE THIS DOCUMENTATION AT A LATER TIME!
    TODO - ADD FOLLOWING EXCEPTION HANDING:
        ConnectionResetError
        socket.error
    :param conn_socket: todo
    :param addr: todo
    """
    conn_socket.send("[INFO] You are now connected to the server".encode())
    while True:
        new_message = conn_socket.recv(1024).decode()
        if new_message:
            to_send = "[{}]: {}".format(addr[0], new_message)
            print(to_send)
            broadcast_message(to_send, conn_socket)

        reply = "OK"

        if new_message == "STOP":
            print("Now exiting client thread for [{}]".format(addr[0]))
            break

        conn_socket.send(reply.encode())

    conn_socket.close()
    print("Connection with [{}] is now closed!".format(addr[0]))


def broadcast_message(message, conn_socket):
    """
    Function to broadcast received message to all clients EXCEPT the one that sent the message.
    :param message: received message from client
    :param conn_socket: client's specific connection socket
    """
    for client in client_list:
        if client != conn_socket:
            try:
                client.send(message.encode())
            except:
                client.close()
                remove_client(client)


def remove_client(conn_socket):
    """
    Helper function removes given connection socket from list of clients.
    :param conn_socket: client's specific connection socket
    """
    if conn_socket in client_list:
        client_list.remove(conn_socket)


def run_server():
    """
    This method runs the multi-threaded server. A new server is initialized and starts listening for incoming
    connections. A single while-loop continues to accept any incoming connections and starts a new thread
    for each individual client that successfully connects. See documentation for client_thread() method for
    more information on what each thread does.
    """
    server = ThreadedServer()
    while True:
        conn, addr = server.accept_connection()
        start_new_thread(client_thread, (conn, addr,))


if __name__ == "__main__":
    run_server()
