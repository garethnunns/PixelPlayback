from PixelPlayback.LogSensorThermo import LogSensorThermo
from PixelPlayback.LogSensorPower import LogSensorPower

logs = [
  LogSensorThermo(5),
  LogSensorPower("/dev/tty.usbserial",5)
]

for log in logs:
  log.start()

try:
  while True:
    pass

except KeyboardInterrupt:
  print("Stopping...")
  for log in logs:
    log.stop()