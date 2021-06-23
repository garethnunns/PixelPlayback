from datetime import datetime
import json
from util import currentTimestamp

# Pixel Playback File
class PPFile:
  def __init__(self, filename=None, source=None):
    # version of how the files are stored
    self.version = 0.2

    self.filename = "" if filename is None else filename
    self.source = "Pixel Playback" if source is None else source

    self.universes = set([])
    self.frames = {}

    # Base output structure
    # all times stored in ms
    self.output = {
      "version": self.version,
      "file": {
        "name": self.filename,
        "created": currentTimestamp(),
        "source": self.source,
        "start": 0,
        "duration": 0
      },
      "universes": list(self.universes),
      "frames": {}
    }

    self.outputDir = "../playback/"


  def addFrame(self, frameNumber, frame):
    self.updateUniverses(frame.dmx)

    # either update the existing frame or add a new one
    if frameNumber not in self.frames:
      self.frames[frameNumber] = frame
    else:
      self.frames[frameNumber].time = frame.time
      self.frames[frameNumber].dmx |= frame.dmx

    # update output
    self.updateFrames()


  def outputFilename(self):
    dateTime = datetime.now()
    filename = dateTime.strftime("%Y-%m-%d__%H-%M-%S")

    if self.filename != "":
      filename = filename + "_" + self.filename

    return filename + '.pp'


  def updateUniverses(self,universes=[]):
    self.universes |= set([uni for uni in universes])

    # update output
    self.output["universes"] = list(self.universes)


  def updateFrames(self):
    self.output["frames"] = {f:self.frames[f].output() for f in self.frames}


  def save(self):
    # update created time
    self.output["file"]["created"] = currentTimestamp()
    
    self.updateUniverses()
    self.updateFrames()

    with open(self.outputDir + self.outputFilename(), "w") as f:
      f.write(json.dumps(self.output, indent=2))


class Frame:
  def __init__(self, time=0, uni=None, dmx=None):
    self.time = time
    self.dmx = {}
    if uni and dmx:
      self.dmx[uni] = dmx

  def output(self):
    return {
      "time": self.time,
      "dmx": self.dmx
    }