"""Interfacing with PZEM
"""

from struct import unpack
import serial

from PixelPlayback.LogSensor import LogSensor

class LogSensorPower(LogSensor):
  """Extends LogSensor to store data from attached PZEM meter
  """
  def __init__(self,com="",frequency=30):
    """Initialise the log with how often you would like the power statistics from the com

    Args:
        com (str, optional): Com port PZEM is connected to. Defaults to "".
        frequency (int, optional): How often to take measurements. Defaults to 30.
    """
    self.com = com
    super().__init__("power", frequency)
  
  def getData(self):
    """Get the data from the PZEM
    """
    # initialise it each time incase connection is lost
    pzem = PZEM(self.com)
    voltage, current, wattage, wattHours = pzem.readAll()

    self.data = {
      "voltage": voltage,
      "current": current,
      "wattage": wattage,
      "wattHours": wattHours
    }

    super().getData()



class PZEM:
  """Interfacing with PZEM
  Code based on by work by Massi from:
  https://www.raspberrypi.org/forums/viewtopic.php?t=124958#p923274

  Raises:
      Exception: Incorrect checksum on response
      serial.SerialTimeoutException: Timeout on PZEM connection
  """
  readVoltageBytes  = [0xB0,0xC0,0xA8,0x01,0x01,0x00,0x1A]
  readCurrentBytes  = [0XB1,0xC0,0xA8,0x01,0x01,0x00,0x1B]
  readWattageBytes  = [0XB2,0xC0,0xA8,0x01,0x01,0x00,0x1C]
  readWattHourBytes = [0XB3,0xC0,0xA8,0x01,0x01,0x00,0x1D]
  setAddrBytes      = [0xB4,0xC0,0xA8,0x01,0x01,0x00,0x1E]

  # dmesg | grep tty  list Serial linux command

  def __init__(self, com="/dev/ttyAMA0", timeout=10.0):
    """Initialise the PZEM and open the serial connection

    Args:
        com (str, optional): Com port to connect to the PZEM. Defaults to "/dev/ttyAMA0".
                             Other common ports include:
                             /dev/ttyUSB0       - USB Serial Port
                             /dev/tty.usbserial - USB Serial Port on a mac
                             /dev/ttyAMA0       - Raspberry Pi port Serial TTL
        timeout (float, optional): Serial maximum timeout in seconds. Defaults to 10.0.
    """

    self.ser = serial.Serial(
      port=com,
      baudrate=9600,
      parity=serial.PARITY_NONE,
      stopbits=serial.STOPBITS_ONE,
      bytesize=serial.EIGHTBITS,
      timeout = timeout
    )

    if self.ser.isOpen():
      self.ser.close()
    self.ser.open()

  def checkChecksum(self, _tuple):
    """Confirms the checksum of the message

    Args:
        _tuple (tuple): Tple containing the message

    Raises:
        Exception: If the checksum does not match

    Returns:
        bool: Whether it matches or not
    """
    _list = list(_tuple)
    _checksum = _list[-1]
    _list.pop()
    _sum = sum(_list)
    if _checksum == _sum%256:
      return True

    raise Exception("Wrong checksum")


  def isReady(self):
    """Checks whether the PZEM is ready to return data

    Raises:
        serial.SerialTimeoutException: Timeout on PZEM connection

    Returns:
        bool: Whether the PZEM is ready or not
    """
    self.ser.write(serial.to_bytes(self.setAddrBytes))
    rcv = self.ser.read(7)
    if len(rcv) == 7:
      unpacked = unpack("!7B", rcv)
      if self.checkChecksum(unpacked):
        return True

    raise serial.SerialTimeoutException("Timeout setting address")


  def readVoltage(self):
    """Read the voltage from the PZEM

    Raises:
        serial.SerialTimeoutException: Timeout on PZEM connection

    Returns:
        float: Voltage (V) as float
    """
    self.ser.write(serial.to_bytes(self.readVoltageBytes))
    rcv = self.ser.read(7)
    if len(rcv) == 7:
      unpacked = unpack("!7B", rcv)
      if self.checkChecksum(unpacked):
        tension = unpacked[2]+unpacked[3]/10.0
        return tension

    raise serial.SerialTimeoutException("Timeout reading tension")


  def readCurrent(self):
    """Read the current from the PZEM

    Raises:
        serial.SerialTimeoutException: Timeout on PZEM connection

    Returns:
        float: Current (A) as float
    """
    self.ser.write(serial.to_bytes(self.readCurrentBytes))
    rcv = self.ser.read(7)
    if len(rcv) == 7:
      unpacked = unpack("!7B", rcv)
      if self.checkChecksum(unpacked):
        current = unpacked[2]+unpacked[3]/100.0
        return current

    raise serial.SerialTimeoutException("Timeout reading current")


  def readWattage(self):
    """Read the wattage from the PZEM

    Raises:
        serial.SerialTimeoutException: Timeout on PZEM connection

    Returns:
        int: Wattage (W) as int
    """
    self.ser.write(serial.to_bytes(self.readWattageBytes))
    rcv = self.ser.read(7)
    if len(rcv) == 7:
      unpacked = unpack("!7B", rcv)
      if self.checkChecksum(unpacked):
        power = unpacked[1]*256+unpacked[2]
        return power

    raise serial.SerialTimeoutException("Timeout reading power")


  def readWattHours(self):
    """Reads the stored watt hours from the PZEM

    Raises:
        serial.SerialTimeoutException: Timeout on PZEM connection

    Returns:
        int: Watt Hours (Wh) as int
    """
    self.ser.write(serial.to_bytes(self.readWattHourBytes))
    rcv = self.ser.read(7)
    if len(rcv) == 7:
      unpacked = unpack("!7B", rcv)
      if self.checkChecksum(unpacked):
        regPower = unpacked[1]*256*256+unpacked[2]*256+unpacked[3]
        return regPower

    raise serial.SerialTimeoutException("Timeout reading registered power")


  def readAll(self):
    """Returns all values (voltage, current, wattage, watt hours)

    Raises:
        serial.SerialTimeoutException: Timeout on PZEM connection

    Returns:
        tuple: All values (voltage, current, wattage, watt hours)
    """
    if self.isReady():
      return(self.readVoltage(),self.readCurrent(),self.readWattage(),self.readWattHours())

    raise serial.SerialTimeoutException("Timeout reading registered power")


  def close(self):
    """Close serial connection to PZEM
    """
    self.ser.close()

# example usage of PZEM
if __name__ == "__main__":
  sensor = PZEM("/dev/tty.usbserial")
  try:
    print("Checking readiness")
    print(sensor.isReady())
    print("Reading voltage")
    print(sensor.readVoltage(),"V")
    print("Reading current")
    print(sensor.readCurrent(),"A")
    print("Reading power")
    print(sensor.readWattage(),"W")
    print("reading registered power")
    print(sensor.readWattHours(),"Wh")
    print("reading all")
    print(sensor.readAll())
  finally:
    sensor.close()