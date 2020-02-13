from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time
from person import Person

#Global variables
HOST = ''
PORT = 33000
ADDR = (HOST, PORT)
MAX_CONNECTIONS = 10
BUFSIZ = 512

#GLOBAL VARIABLES
persons = []
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR) #set up server

def broadcast(msg, name):
	"""
	Send new messages to all clients
	:param msg: bytes["utf8"]
	:param name: str
	"""
	for person in persons:
		client = person.client
		client.send(bytes(name + ": ", "utf8") + msg)


def client_communication(person):
    """
    Thread to handle all messages from clients
    :param person: socket
    :return: None
    """
    client = person.client
    addr = person.addr

    #get persons name
    name = client.recv(BUFSIZ).decode("utf8")
    welcome = f"Welcome {name}! To quit chat, enter quit."
    joined = f"{name} has joined the chat!"
    client.send(bytes(welcome, name))
    broadcast(joined) #broadcast welcome message

    while True:
        msg = client.recv(BUFSIZ).decode("utf8")
        if msg == bytes("{quit}", "utf8"):
        	client.send(bytes("{quit}", "utf8"))
            broadcast(bytes(f"{name} has left the chat.", name))
            client.close()
            persons.remove(person)
        else:
        	client.send(msg, name)



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
            client, addr = server.accept()
            person = Person(addr, name, client)
            persons.append(person)
            print(f"[CONNECTION ] {addr} connected to the server at {time.time()}")
            Thread(target=client_communication, args=(person,)).start()
        except Exception as e:
            print("Failed: ", e)
            run = False
    print("SERVER CRASHED")


if __name__ == "__main__":
    SERVER.listen(MAX_CONNECTIONS) #listen for connections
    print("[STARTED] Waiting for connection...")
    ACCEPT_THREAD = Thread(target=wait_for_connection)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()