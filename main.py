from PixelPlayback.LogSensorThermo import LogSensorThermo

logs = [
  LogSensorThermo(3)
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