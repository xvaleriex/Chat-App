import time

from client import Client
from threading import Thread


c1 = Client("Val")
c2 = Client("Rosalka")


def update_messages():
	msgs = []
	run = True
	while run:
		time.sleep(0.1) 
		new_msgs = c1.get_messages()
		msgs.extend(new_msgs)

		for msg in new_msgs:
			print(msg)
			if msg == "quit":
				run = False
				break


Thread(target=update_messages).start()

c1.send_message("Hello")
time.sleep(2)
c2.send_message("Meooow")
time.sleep(2)
c1.send_message("Lets go eat")
time.sleep(2)
c2.send_message("Meooow")
time.sleep(2)
c1.disconnect()
time.sleep(2)
c2.disconnect()