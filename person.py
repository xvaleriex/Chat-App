class Person:
	"""
	Class that represents person
	holds client socket, addr and name
	"""
	def __init__(self, addr, client):
		self.addr = addr
		self.client = client
		self.name = None

	def set_name(self, name):
		"""
		Sets the name for a person
		:param name: bytes
		:return:
		"""
		self.name = name


	def __repr__(self):
		return f"Person({self.addr}. {self.name})"


