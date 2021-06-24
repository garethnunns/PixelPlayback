import glob
import time
from PixelPlayback.Log import Log
from PixelPlayback.util import filePathToFileName

class LogThermo(Log):
  def __init__(self,frequency=30):
    super().__init__("thermo", frequency)

  def getData(self):
    baseDir = '/sys/bus/w1/devices/'
    devices = glob.glob(baseDir + '28*')
    deviceFile = '/w1_slave'

    if len(devices) == 0:
      raise Exception("No temperature sensors connected")

    for device in devices:
      with open(device + deviceFile, 'r') as f:
        lines = f.readlines()

        # wait for the data to become available
        while lines[0].strip()[-3:] != 'YES':
          time.sleep(0.2)
          lines = f.readlines()

        # get the temperature
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
          temp_string = lines[1][equals_pos+2:]
          temp = float(temp_string) / 1000.0
          self.data[filePathToFileName(device)] = temp

    super().getData()