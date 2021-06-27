from PixelPlayback.Log import Log
from PixelPlayback.TimerInterval import TimerInterval

class LogSensor(Log):
  """Extends the Log class and get it be runs on loop (usually for logging sensor data)
  """
  def __init__(self, name="", logFrequency=30):
    """Create a new log for a sensor, preferably with a name and how often you want to log it

    Args:
        name (str, optional): Name of the log. Defaults to "".
        logFrequency (int, optional): How often you want to log the data (in seconds).
        Defaults to 30.
    """
    super().__init__(name)

    self.timer = None
    self.logFrequency = logFrequency

  def getData(self):
    """to be overriden in subclass as the method for getting the data from the sensor
    This needs to call super().getData() at the end
    """
    self.writeData()

  def getDataCatcher(self):
    """Catches any errors in the getData method and logs them
    """
    try:
      self.getData()
    except Exception as e:
      self.writeData(False,{"error":str(e)})

  def start(self):
    """Starts the logging at the specified frequency
    """
    # then keep logging (until stopped)
    self.timer = TimerInterval(self.logFrequency, self.getDataCatcher)
    self.timer.start()

  def stop(self):
    """Stops the logging
    """
    if self.timer is not None:
      self.timer.cancel()