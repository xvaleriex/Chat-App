from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

#GLOBAL CONSTANTS
HOST = "localhost"
PORT = 5500
ADDR = (HOST, PORT)
BUFSIZ = 512

#GLOBAL VARIABLES
messages = []

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)


def recieve_messages():
	"""
	Recieve mesagges from server
	"""
	while True:
		try:
			msg = client_socket.recv(BUFSIZ).decode("utf8")
			messages.append(msg)
			print(msg)
		except Exception as e:
			print("[EXCEPTION]", e)
			break


def send_message(msg):
	"""
	Send messages to server
	:param msg: str 
	"""	
	client_socket.send(bytes(msg, "utf8"))
	if msg == "{quit}":
		client_socket.close()


client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()

send_message("Valinka")
send_message("Hello")
