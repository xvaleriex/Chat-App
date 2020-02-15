import time
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import errno
from signal import signal, SIGPIPE, SIG_DFL

#GLOBAL CONSTANTS
HOST = "localhost"
PORT = 5600
ADDR = (HOST, PORT)
BUFSIZ = 512

#GLOBAL VARIABLES
messages = []

signal(SIGPIPE,SIG_DFL)
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

receive_thread = Thread(target=recieve_messages)
receive_thread.start()

try:
	send_message("Valinka")
	time.sleep(1)
	send_message("Hello")
	time.sleep(1)
except socket.error as e:
	if isinstance(e.args, tuple):
		print("errno is %d" % e[0])
		if e[0] == errno.EPIPE:
			# remote peer disconnected
			print("Detected remote disconnect")
		else:
			# determine and handle different error
			pass
	else:
		print
		"socket error ", e
	client_socket.close()


