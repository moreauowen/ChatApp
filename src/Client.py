"""
Client.py
@author Owen Moreau
"""
import socket

client_name = socket.gethostname()
server_name = "10.220.74.108"
server_port = 5000

client_message = input(" -> ")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_name, server_port))

print("[INFO]: Now connected to {}!".format(server_name))

while client_message != "STOP":
    try:
        client_socket.send(client_message.encode())
        server_message = client_socket.recv(1024)
    except Exception as err:
        print("Error found, exiting connection now. Error: {}".format(err))
        break

    print("[SERVER]: {}".format(server_message.decode()))

    client_message = input(" -> ")

client_socket.send(client_message.encode())
client_socket.close()
print("[INFO]: The connection between {} and {} is now closed!".format(client_name, server_name))