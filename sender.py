import sacn
import time
import netifaces
import json
from threading import Timer

class ResettableTimer(object):
    def __init__(self, interval, function, args):
        self.interval = interval
        self.function = function
        self.args = args
        self.timer = Timer(self.interval, self.function, args)

    def start(self):
        self.timer.start()

    def restart(self):
        self.timer.cancel()
        self.timer = Timer(self.interval, self.function, self.args)
        self.timer.start()

    def cancel(self):
      self.timer.cancel()
      self.timer = Timer(self.interval, self.function, self.args)

class Playback:
  def __init__(self,filename=None, iface='lo0'):
    self.iface = iface

    # server IP
    self.IP = netifaces.ifaddresses(self.iface)[netifaces.AF_INET][0]['addr']

    # generate CID based on IP - this could be improved
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

    if self.filename != None:
      self.loadFile()


  def loadFile(self, filename=None):
    if filename is None:
      filename = self.filename

    self.recording = json.load(open(filename))

    # store the universes that we will output
    self.universes = [int(i) for i in self.recording['universes']]

    self.activateUniverses()

    # if the DMX has been recorded, normalised the times
    if self.recording['start'] > 0:
      for frame in self.recording['frames']:
        self.recording['frames'][frame]['time'] -= self.recording['start']
        # convert from ms to seconds
        self.recording['frames'][frame]['time'] /= 1000

        frameTime = self.recording['frames'][frame]['time']

        # load all the frames into timers ready to send
        self.timers[frame] = ResettableTimer(frameTime, self.send, [frame])

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

      self.recording['start'] = 0

    #TODO: add _event emitter_
    self.play()


  def activateUniverses(self,universes=None):
    if universes is None:
      universes = self.universes

    for uni in self.universes:
      self.server.activate_output(uni)
      self.server[uni].multicast = True
      self.server


  def deactivateUniverses(self,universes=None):
    if universes is None:
      universes = self.server.get_active_outputs()

    for uni in self.universes:
      self.server.deactivate_output(uni)


  def play(self, loop=True):
    for timer in self.timers:
      self.timers[timer].restart()

    if loop:
      del self.timerLoop
      self.timerLoop = Timer(self.duration, self.play)
      self.timerLoop.start()


  def send(self,frame=None):
    if frame is None:
      return

    print(frame)

    # loop through the universes in that frame
    for uni in self.recording['frames'][frame]['dmx']:
      self.server[uni].dmx_data = self.recording['frames'][frame]['dmx'][uni]

    self.server.flush()


  def close(self):
    self.server.stop()


playback = Playback('playback/1624230670575.json','en6')
playback.close()