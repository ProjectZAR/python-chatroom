import socket
import threading

# Funktion für jeden Client-Thread
def handle(client):
    name = client.recv(1024).decode("utf8")
    welcome = "Willkommen %s! Wenn du den Chat verlassen möchtest, gib 'quit' ein." % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s ist beigetreten!" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name

    while True:
        msg = client.recv(1024)
        if msg != bytes("quit", "utf8"):
            broadcast(msg, name+": ")
        else:
            client.send(bytes("quit", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s hat den Chat verlassen." % name, "utf8"))
            break

# Broadcast-Funktion für Nachrichten
def broadcast(msg, prefix=""):
    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)

# Hauptprogramm
clients = {}

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 8080))
server.listen()

print("Chatroom-Server gestartet")

while True:
    client, addr = server.accept()
    print("%s hat sich verbunden." % str(addr))
    client.send(bytes("Gib deinen Nickname ein:", "utf8"))
    client_thread = threading.Thread(target=handle, args=(client,))
    client_thread.start()

server.close()
