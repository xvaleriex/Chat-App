import time
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread, Lock
import errno
from signal import signal, SIGPIPE, SIG_DFL


class Client:
    """
    For communication with server
    """

    # GLOBAL CONSTANTS
    HOST = "localhost"
    PORT = 5600
    ADDR = (HOST, PORT)
    BUFSIZ = 512

    def __init__(self, name):
        """
        Init object and send name to server
        :param name: str
        """
        # signal(SIGPIPE, SIG_DFL)
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(self.ADDR)
        self.messages = []
        recieve_thread = Thread(target=self.recieve_messages)
        recieve_thread.start()
        self.send_message(name)
        self.lock = Lock()

    def recieve_messages(self):
        """
        Recieve mesagges from server
        """
        while True:
            try:
                msg = self.client_socket.recv(self.BUFSIZ).decode()

                # make sure memory is safe to access
                self.lock.acquire()
                self.messages.append(msg)
                self.lock.release()
            except Exception as e:
                print("[EXCEPTION CLIENT]", e)
                break

    def send_message(self, msg):
        """
        Send messages to server
        :param msg: str
        """
        try:
            self.client_socket.send(bytes(msg, "utf8"))
            if msg == "quit":
                self.client_socket.close()
        except Exception as e:
            self.client_socket = socket(AF_INET, SOCK_STREAM)
            self.client_socket.connect(self.ADDR)
            print(e)

    def get_messages(self):
        """
        Return list of messages
        :return: list[]
        """
        messages_copy = self.messages[:]

        # make sure memory is safe to access
        self.lock.acquire()
        self.messages = []
        self.lock.release()

        return messages_copy

    def disconnect(self):
        self.send_message("quit\r\n")
