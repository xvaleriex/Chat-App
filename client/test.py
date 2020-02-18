from client import client
from threading inmport Thread

c1 = Client("Val")
c2 = Client("Rosalka")

c1.send_message("Hello")
time.sleep(2)
c2.send_message("Meooow")
time.sleep(2)
c1.send_message("Lets go eat")
time.sleep(2)
c2.send_message("Meooow")
time.sleep(5)

c1.disconnect()
time.sleep(2)
c2.disconnect()


def update_messages():
	while True:
		time.sleep(0.1)
		msgs = c1.get_messages()