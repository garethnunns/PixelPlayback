from PixelPlayback.Playback import Playback

playback = Playback('user/playback/2021-06-23__20-20-11_Demo v002_Lossless.pp','en0')

try:
  while True:
    pass

except KeyboardInterrupt:
  print("Stopping...")
  playback.stop()