from e5052b_driver.e5052b_I import E5052BInterface
import vxi11
from enum import Enum

# class FREQ_B(Enum):
# 	B1 = "BAND1"
# 	B2 = "BAND2"
# 	B3 = "BAND3"
# 	B4 = "BAND4"
# 	B5 = "BAND5"
# 	B1 = "BAND6"

AM_BANDS = [(0, 0), (60e6, 111e6), (109e6, 1.5e9), (250e6, 3e9)]
PN_BANDS = [(10e6, 41e6), (39e6, 101e6), (99e6, 1.5e9), (250e6, 3e9)]

START_FREQS = [1, 10, 100, 1e3]
PN_STOP_FREQS = [100e3, 1e6, 5e6, 10e6, 20e6, 40e6, 100e6]
AM_STOP_FREQS = [100e3, 1e6, 5e6, 10e6, 20e6, 40e6]

class E5052B(E5052BInterface):

	def __init__(self, ip: str):
		self._dev_ip = ip
		self._dev = vxi11.Instrument(ip)

	async def get_id(self) -> None:
		return self._dev.ask("*IDN?")

	async def init_pn_meas(self, off_start: float, off_end: float, nom_freq: float):
		self._dev.write(":TRIGger:MODE PN1")
		self._dev.write(":INITiate:PN1:CONTinuous OFF")

		band = self.get_band_no(nom_freq, PN_BANDS)
		if band == 0:
			return -1
		self._dev.write(f":SENSe:PN1:FBANd BAND{band}")

		if off_start not in START_FREQS or off_end not in PN_STOP_FREQS:
			return -1
		self._dev.write(f":SENSe:PN1:FREQuency:STARt {off_start}")
		self._dev.write(f":SENSe:PN1:FREQuency:STOP {off_end}")

		self._dev.write(":INITiate:PN1:IMMediate")
		return 0

	async def init_am_meas(self, off_start: float, off_end: float, nom_freq: float):
		self._dev.write(":TRIGger:MODE AM1")
		self._dev.write(":INITiate:AM1:CONTinuous OFF")
		
		band = self.get_band_no(nom_freq, AM_BANDS)
		if band == 0:
			return -1
		self._dev.write(f":SENSe:AM1:FBANd BAND{band}")

		if off_start not in START_FREQS or off_end not in AM_STOP_FREQS:
			return -1
		self._dev.write(f":SENSe:AM1:FREQuency:STARt {off_start}")
		self._dev.write(f":SENSe:AM1:FREQuency:STOP {off_end}")

		self._dev.write(":INITiate:AM1:IMMediate")
		return 0

	async def get_pn_data(self):
		x_data = [float(val) for val in self._dev.ask(":CALCulate:PN1:DATA:XDATA?").split(",")]
		p_data = [float(val) for val in self._dev.ask(":CALCulate:PN1:DATA:PDATA?").split(",")] #TODO Check if RDATA is better
		carr = [float(val) for val in self._dev.ask(":CALCulate:PN1:DATA:CARRier?").split(",")]
		return carr[0], carr[1], x_data, p_data
	
	async def get_am_data(self):
		x_data = [float(val) for val in self._dev.ask(":CALCulate:AM1:DATA:XDATA?").split(",")]
		p_data = [float(val) for val in self._dev.ask(":CALCulate:AM1:DATA:PDATA?").split(",")] #TODO Check if RDATA is better
		carr = [float(val) for val in self._dev.ask(":CALCulate:AM1:DATA:CARRier?").split(",")]
		return carr[0], carr[1], x_data, p_data

	def get_band_no(self, freq: float, bands: list[tuple[float, float]]) -> int:
		for i, b in enumerate(bands):
			if freq >= b[0] and freq <= b[1]:
				return i + 1
		return 0
