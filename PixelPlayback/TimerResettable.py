from threading import Timer

#TODO: could rewrite to match style of TimerInterval

class TimerResettable():
  """Like a Timer, only resetable
  """
  def __init__(self, interval, function, args):
    """Initialise a new Timer with the standard args

    Args:
        interval (int): Time delay for Timer in seconds
        function (function): Function to be run by Timer
        args (args): Arguments to be passed to the Timer
    """
    self.interval = interval
    self.function = function
    self.args = args
    self.timer = Timer(self.interval, self.function, args)

  def start(self):
    """Start the timer
    """
    self.timer.start()

  def restart(self):
    """Restart the timer with
    """
    self.timer.cancel()
    self.timer = Timer(self.interval, self.function, self.args)
    self.timer.start()

  def cancel(self):
    """Stop the timer
    """
    self.timer.cancel()
    self.timer = Timer(self.interval, self.function, self.args)