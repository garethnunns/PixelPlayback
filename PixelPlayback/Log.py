import json
import os

from PixelPlayback.Util import DIR_LOGS, currentTimestamp, currentUTC, outputFilename, dictKeysToCSV, dictValuesToCSV

class Log:
  """Handy way to log data
  """
  def __init__(self,name=""):
    """Initialse the log, ideally with a name

    Args:
        name (str, optional): Name of the log - will determine folder & file name. Defaults to "".
    """
    self.name = name

    # all logging is in /user/logs/[name]
    self.logFolder = os.path.join(DIR_LOGS, self.name)

    # create the folder if it doesn't exist
    if not os.path.exists(self.logFolder):
      os.makedirs(self.logFolder)

    self.data = {}

  def writeData(self,success=True,data=None):
    """Write data to the log

    Args:
        success (bool, optional): Whether what you're logging has been successful. Defaults to True.
        data (dict, optional): The data to log - converted to JSON & CSV. Defaults to None.
    """
    if data is None:
      data = self.data

    data = {"data": data}

    data["_success"] = success

    data["_time"] = {
      "unix": currentTimestamp(),
      "utc": currentUTC()
    }

    # create today's logging file (JSON)
    with open(os.path.join(self.logFolder, outputFilename(self.name, "pp.log.jsonl", False)), 'a+') as f:
      f.write(json.dumps(data, sort_keys=True) + "\n")

    # create today's logging file (CSV)
    with open(os.path.join(self.logFolder, outputFilename(self.name, "pp.log.csv", False)), 'a+') as f:
      # add the headings for the data at the top (and assume they stay the same)
      if f.tell() == 0:
        f.write(dictKeysToCSV(data) + "\n")
      f.write(dictValuesToCSV(data) + "\n")

    # clear data after it has been writted
    self.data = {}