import abc

class E5052BInterface(abc.ABC):

	@abc.abstractmethod
	async def get_id(self) -> str:
		"""Identify the device
		
		Returns
			- str - device identificator
		"""

	@abc.abstractmethod
	async def init_pn_meas(self, off_start: float, off_end: float, nom_freq: float) -> None:
		"""Initialise phase noise measurement
		
		Arguments
			- off_start - starting offset frequency [Hz]
			- off_end - ending offset frequency [Hz]
			- nom_freq - expected carrier frequency [Hz]
		"""

	@abc.abstractmethod
	async def init_am_meas(self, off_start, off_end, nom_freq) -> None:
		"""Initialise amplitude noise measurement
	
		Arguments
			- off_start - starting offset frequency [Hz]
			- off_end - ending offset frequency [Hz]
			- nom_freq - expected carrier frequency [Hz]
		"""

	@abc.abstractmethod
	async def get_pn_data(self) -> tuple[float, float, list[float], list[float]]:
		"""Read data of the last PN measurement
		
		Returns
			- float - carrier frequency
			- float - carrier power
			- list[float] - offset frequencies [Hz]
			- list[float] - noise density values [dBc/Hz]
		"""

	@abc.abstractmethod
	async def get_am_data(self) -> tuple[float, float, list[float], list[float]]:
		"""Read data of the last AM noise measurement
		
		Returns
			- float - carrier frequency
			- float - carrier power
			- list[float] - frequency points [Hz]
			- list[float] - noise density values [dBc/Hz]
		"""

