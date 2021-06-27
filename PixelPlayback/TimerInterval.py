from threading import Timer

class TimerInterval(Timer):
  """Extends Timer class, similar to JS' setInterval, allows you to run a Timer on loop
  """
  def run(self):
    """Run the specified function on loop
    """
    # first run the function immeadiately
    self.function(*self.args, **self.kwargs)

    # the run it on loop
    while not self.finished.wait(self.interval):
      self.function(*self.args, **self.kwargs)