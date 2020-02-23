from os import name
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time
from person import Person

# Global variables
HOST = '0.0.0.0'
PORT = 5600
ADDR = (HOST, PORT)
MAX_CONNECTIONS = 10
BUFSIZ = 512

# GLOBAL VARIABLES
persons = []
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)  # set up server


def broadcast(msg, name1):
    """
    Send new messages to all clients
    :param msg: bytes["utf8"]
    :param name1: str
    """
    for person in persons:
        client = person.client
        try:
            client.send(bytes(name1, "utf8") + msg)
        except Exception as e:
            print("[EXCEPTION BROADCAST]", e)


def client_communication(person):
    """
    Thread to handle all messages from clients
    :param person: socket
    :return: None
    """
    client = person.client

    # get persons name
    client_name = client.recv(BUFSIZ).decode("utf8")
    person.set_name(client_name)

    welcome = bytes(f"Welcome {client_name}!To quit chat, enter quit.\n", "utf8")
    joined = bytes(f"{client_name}has joined the chat!\n", "utf8")
    client.send(welcome)
    broadcast(joined, "")  # broadcast welcome message

    while True: #wait for any messages from person
        try:
            msg = client.recv(BUFSIZ)
            if msg == bytes("quit\r\n", "utf8"): #if message is quit, disconnect client
                client.close()
                persons.remove(person)
                broadcast(bytes(f"{client_name} has left the chat.\n", "utf8"), "")
                print(f"[DISCONNECTED] {client_name}")
            else: # otherwise send message to all clients
                broadcast(msg, client_name + ": ")
                print(f"{name}: ", msg.decode("utf8"))
        except Exception as e:
            print("[EXCEPTION COMMUNICATION]", e)
            break


def wait_for_connection():
    """
    Wait for connection from new clients,
    start new thread once connected
    :param server: SOCKET
    :return: None
    """
    run = True
    while run:
        try:
            client, addr = SERVER.accept()
            person = Person(addr, client) # create new person for connection
            persons.append(person)

            print(f"[CONNECTION ] {addr} connected to the server at {time.time()}")
            Thread(target=client_communication, args=(person,)).start()
        except Exception as e:
            print("[EXCEPTION WAIT FOR CONN]", e)
            run = False
    print("SERVER CRASHED")


if __name__ == "__main__":
    SERVER.listen(MAX_CONNECTIONS)  # listen for connections
    print("[STARTED] Waiting for connection...")
    ACCEPT_THREAD = Thread(target=wait_for_connection)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
