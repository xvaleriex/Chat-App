from client import client
from threading inmport Thread

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
			if msg == "quit\r\n":
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
time.sleep(5)

c1.disconnect()
time.sleep(2)
c2.disconnect()