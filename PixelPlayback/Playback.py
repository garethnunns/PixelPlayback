import json
from threading import Timer
import netifaces
import sacn

from PixelPlayback.TimerResettable import TimerResettable

class Playback:
  """Playback of .pp over sACN
  """
  def __init__(self,filename, iface='lo0'):
    """Initalise the player with the filename and the network interface

    Args:
        filename (str): .pp file to playback
        iface (str, optional): network interface to output sACN. Defaults to 'lo0'.
    """
    self.iface = iface

    # server IP
    self.IP = netifaces.ifaddresses(self.iface)[netifaces.AF_INET][0]['addr']

    # generate CID based on IP
    # TODO: improve this method
    self.CID = [ord(char) for char in "gareth nunns"]  + [int(char) for char in self.IP.split(".")]

    self.sourceName = "Pixel Playback"

    self.server = sacn.sACNsender(self.IP, 5568, self.sourceName, tuple(self.CID), 25, True)

    # start the sending thread
    self.server.start()

    # we will manually flush as this gives sync as well
    self.server.manual_flush = True

    # store for the universes we will output to
    self.universes = []

    self.recording = {}
    self.timers = {}
    self.timerLoop = None
    self.duration = 0

    self.filename = filename

    if self.filename is not None:
      self.loadFile()


  def loadFile(self, filename=None):
    """Load the file into the player

    Args:
        filename (str, optional): .pp file to playback. Defaults to None.
    """
    print("Loading ", self.filename)

    if filename is None:
      filename = self.filename

    # load the file
    # TODO: catch if file does not exist
    self.recording = json.load(open(filename))

    # store the universes that we will output
    self.universes = [int(i) for i in self.recording['universes']]

    self.activateUniverses()

    for frame in self.recording['frames']:
      print("Loading frame ", frame)
       # if the DMX has been recorded, normalised the times
      if self.recording['file']['start'] > 0:
        self.recording['frames'][frame]['time'] -= self.recording['file']['start']

      # convert from ms to seconds
      self.recording['frames'][frame]['time'] /= 1000

      frameTime = self.recording['frames'][frame]['time']

      # load all the frames into timers ready to send
      self.timers[frame] = TimerResettable(frameTime, self.send, [frame])

      # keep track of the duration
      self.duration = self.recording['frames'][frame]['time']

      # convert universe to int from str
      self.recording['frames'][frame]['dmx'] = {int(uni):data for uni, data in self.recording['frames'][frame]['dmx'].items()}

      # wrangle the frames into tuples that the sACN library likes
      for uni in self.recording['frames'][frame]['dmx']:
        # check it's in the activated outputs
        if uni in self.server.get_active_outputs():
          # what an excellent one liner
          self.recording['frames'][frame]['dmx'][uni] = tuple(self.recording['frames'][frame]['dmx'][uni][str(ch)] if str(ch) in self.recording['frames'][frame]['dmx'][uni] else 0 for ch in range(1,512))

    self.recording['file']['start'] = 0

    #TODO: add _event emitter_
    self.play()


  def activateUniverses(self,universes=None):
    """Active the universes so they're ready to output sACN

    Args:
        universes (list, optional): List of universes to activate. Defaults to None.
    """
    if universes is None:
      universes = self.universes

    for uni in self.universes:
      self.server.activate_output(uni)
      self.server[uni].multicast = True


  def deactivateUniverses(self,universes=None):
    """Deactivate the universes so they no longer send sACN

    Args:
        universes (list, optional): List of universes to deactivate. Defaults to None.
    """
    if universes is None:
      universes = self.server.get_active_outputs()

    for uni in self.universes:
      self.server.deactivate_output(uni)


  def play(self, loop=True):
    """Start playing back the loaded file

    Args:
        loop (bool, optional): Whether or not to loop playback. Defaults to True.
    """
    for timer in self.timers:
      self.timers[timer].restart()

    if loop:
      del self.timerLoop
      self.timerLoop = Timer(self.duration, self.play)
      self.timerLoop.start()


  def send(self,frame):
    """Send an individual frame via sACN

    Args:
        frame (Frame, optional): Frame to be sent
    """
    print(frame)

    # loop through the universes in that frame
    for uni in self.recording['frames'][frame]['dmx']:
      self.server[uni].dmx_data = self.recording['frames'][frame]['dmx'][uni]

    self.server.flush()


  def stop(self):
    """Stops playback and the sACN server
    """
    self.timerLoop.cancel()

    for timer in self.timers:
      self.timers[timer].cancel()

    self.server.stop()