from PixelPlayback.LogThermo import LogThermo

logs = [
  LogThermo(3)
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