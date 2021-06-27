import json
import os

from PixelPlayback.Util import DIR_PLAYBACK, currentTimestamp, outputFilename

# Pixel Playback File
class PPFile:
  """A Pixel Playback (.pp) file, used to store/playback DMX universe(s)
  """
  def __init__(self, filename="", generator="Pixel Playback", source=""):
    """Initialise a new .pp file to create

    Args:
        filename (str, optional): File name of the file to create. Defaults to "".
        generator (str, optional): The generator/converter of the DMX data. Defaults to "Pixel Playback".
        source (str, optional): The original source of DMX data (e.g. video file name/console name). Defaults to "".
    """
    # version of how the files are stored
    self.version = 0.2

    self.filename = filename
    self.generator = generator
    self.source = source

    self.universes = set([])
    self.frames = {}

    # Base output structure
    # all times stored in ms
    # TODO: this should probably be a function so all values get updated at the time of output
    self.output = {
      "version": self.version,
      "file": {
        "name": self.filename,
        "created": currentTimestamp(),
        "generator": self.generator,
        "source": self.source,
        "start": 0,
        "duration": 0
      },
      "universes": list(self.universes),
      "frames": {}
    }

    self.outputDir = DIR_PLAYBACK


  def addFrame(self, frameNumber, frame):
    """Add a frame to the file

    Args:
        frameNumber (int): Number of the frame in the recording (could be based off the sequence number for DMX recordings)
        frame (Frame): A Frame containing the DMX data
    """
    self.updateUniverses(frame.dmx)

    # either update the existing frame or add a new one
    if frameNumber not in self.frames:
      self.frames[frameNumber] = frame
    else:
      self.frames[frameNumber].time = frame.time
      self.frames[frameNumber].dmx |= frame.dmx

    # update output
    self.updateFrames()


  def updateUniverses(self,universes=None):
    """Update internal stores of the universes which are being recorded

    Args:
        universes (list, optional): List of additional universes being recorded as ints.
        Defaults to None.
    """
    universes = [] if universes is None else universes

    self.universes |= set([int(uni) for uni in universes])

    # update output
    self.output["universes"] = list(self.universes)


  def updateFrames(self):
    """Update the frames in the output to only contain the output of the 
    Frame objects in PPFile.frames
    """
    self.output["frames"] = {f:self.frames[f].output() for f in self.frames}


  def save(self):
    """Save the file with the specifed filename
    """

    # update created time
    self.output["file"]["created"] = currentTimestamp()
    
    self.updateUniverses()
    self.updateFrames()

    with open(os.path.join(self.outputDir + outputFilename(self.filename, "pp")), "w") as f:
      f.write(json.dumps(self.output, indent=2))