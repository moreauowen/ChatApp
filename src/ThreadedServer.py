"""
ThreadedServer.py
@author Owen Moreau
"""
import socket
server_name = socket.gethostname()
server_port = 5000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("",server_port))
server_socket.listen(1)
print("[INFO]: Starting server for chat application - address {}.".format(socket.gethostname()))

connection_socket, addr = server_socket.accept()
client_name = addr[0]
client_port = addr[1]
print("[INFO]: Now connected to {}:{}!".format(str(client_name),str(client_port)))

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
