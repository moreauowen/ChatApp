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


class ThreadedServer:
    def __init__(self):
        self.server_addr = socket.gethostbyname(socket.gethostname())
        self.server_port = 5000
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.server_addr, self.server_port))
        self.server_socket.listen(1)
        print("[INFO]: Starting server for chat application - address:{}, port:{}.".format(self.server_addr,
                                                                                           self.server_port))
        print("________________________________________________________________________________________")

    def __str__(self):
        print_server = "Chat Application Server - HOST:{}, PORT:{}".format(self.server_addr, self.server_port)
        return print_server

    def accept_connection(self):
        connection_socket, addr = self.server_socket.accept()
        client_list.append(connection_socket)

        print("[INFO]: Client connected from {}:{}!".format(str(addr[0]), str(addr[1])))
        return connection_socket, addr


def client_thread(conn_socket, addr):
    conn_socket.send("WELCOME TO SERVER!".encode())

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

        conn_socket.sendall(reply.encode())

    conn_socket.close()
    print("Connection with [{}] is now closed!".format(addr[0]))


def broadcast_message(message, conn_socket):
    for client in client_list:
        if client != conn_socket:
            try:
                client.send(message.encode())
            except:
                client.close()
                remove_client(client)


def remove_client(conn_socket):
    if conn_socket in client_list:
        client_list.remove(conn_socket)
        #print("[INFO] Just removed {} from list of clients!".format(conn_socket.gethostbyname(conn_socket.gethostname())))


def receive_message():
    """
    print()
    client_message = connection_socket.recv(1024)
    while client_message.decode() != "STOP":
        print("[CLIENT]: {}".format(client_message.decode()))
        server_message = input(" -> ")
        try:
            connection_socket.send(server_message.encode())
            client_message = connection_socket.recv(1024)
        except ConnectionAbortedError as err:
            print("[INFO]: The connection was aborted by client {}. Closing the connection now.".format(client_name))
            break

    server_socket.close()
    print("[INFO]: The connection between {} and {} is now closed!".format(client_name, server_name))
    """


def run_server():
    server = ThreadedServer()
    while True:
        conn, addr = server.accept_connection()
        start_new_thread(client_thread, (conn,addr,))


if __name__ == "__main__":
    run_server()
