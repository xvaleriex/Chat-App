from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time

#Global variables
HOST = ''
PORT = 33000
ADDR = (HOST, PORT)
MAX_CONNECTIONS = 10
BUFSIZ = 512

def broadcast()

def client_communication(client):
    """
    Thread to handle all messages from clients
    :param client: socket
    :return: None
    """
    run = True
    while run:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            client.close()
        else:



def wait_for_connection(server):
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
            #todo : google about that f
            print(f"[CONNECTION ] {addr} connected to the server at {time.time()}")
            Thread(target=client_communication, args=(client,)).start()
        except Exception as e:
            print("Failed: ", e)
            run = False
    print("SERVER CRASHED")


SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(MAX_CONNECTIONS) #listen for connections
    print("[STARTED] Waiting for connection...")
    ACCEPT_THREAD = Thread(target=wait_for_connection)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()