class Frame:
  """Store single frame of multiple DMX universes, usually used in the construction of a .pp file
  """
  def __init__(self, time=0, uni=None, dmx=None):
    """Create a frame, possibly including the first universe to be stored

    Args:
        time (int, optional): Time from the start in ms the frame is to be played back. Defaults to 0.
        uni (int, optional): Universe to be stored in the Frame.dmx. Defaults to None.
        dmx (dict, optional): The DMX data stored in the Frame.dmx[uni]. Dict structured like {[ch]: [value]}. Defaults to None.
    """
    self.time = time
    self.dmx = {}
    if uni and dmx:
      self.dmx[uni] = dmx

  def output(self):
    """Returns a dict with only the necessary information to be stored (time & DMX).
    Useful as the class may have other attributes that don't need to be stored in the .pp file

    Returns:
        dict: Dict with the format {"time": 123456, "dmx: {[uni]: {[ch]: [value]} } }
    """
    return {
      "time": self.time,
      "dmx": self.dmx
    }