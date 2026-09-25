from e5052b_I import E5052BInterface
import vxi11

class E5052B(E5052BInterface):

	def __init__(self, ip: str):
		self._dev = vxi11.Instrument(ip)

	