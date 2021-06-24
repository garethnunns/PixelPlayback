import os
import json
from util import currentTimestamp, currentUTC, outputFilename, SetInterval, dictKeysToCSV, dictValuesToCSV

import time #remove

class Log:
  def __init__(self,name="",logFrequency=30):
    self.name = name
    self.logFrequency = logFrequency

    # all logging is in /user/logs/[name]
    self.logFolder = os.path.join(os.path.dirname(__file__), '..', 'user', 'logs', self.name)

    # create the folder if it doesn't exist
    if not os.path.exists(self.logFolder):
        os.makedirs(self.logFolder)

    self.timer = None
    self.data = {}

  def writeData(self,data=None):
    if data is None:
      data = self.data

    data["time"] = {
      "unix": currentTimestamp(),
      "utc": currentUTC()
    }

    # create today's logging file (JSON)
    with open(os.path.join(self.logFolder, outputFilename(self.name, "pp.log.jsonl", False)), 'a+') as f:
      f.write(json.dumps(data) + "\n")

    # create today's logging file (CSV)
    with open(os.path.join(self.logFolder, outputFilename(self.name, "pp.log.csv", False)), 'a+') as f:
      # add the headings for the data at the top (and assume they stay the same)
      if f.tell() == 0:
        f.write(dictKeysToCSV(data) + "\n")
      f.write(dictValuesToCSV(data) + "\n")

  def getData(self):
    # to be overriden in subclass
    self.writeData()

  def start(self):
    # immeadiately do a log
    self.getData()

    # then keep logging (until stopped)
    self.timer = SetInterval(self.logFrequency, self.getData)
    self.timer.start()

  def stop(self):
    if self.timer != None:
      self.timer.cancel()