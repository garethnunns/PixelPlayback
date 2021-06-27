"""Utility functions used in module
"""

from datetime import datetime
import os

# paths
DIR_USER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'user'))
DIR_LOGS = os.path.join(DIR_USER, "logs")
DIR_MAPPING = os.path.join(DIR_USER, "mapping")
DIR_PLAYBACK = os.path.join(DIR_USER, "playback")


def currentTimestamp():
  """Returns current Unix epoch time

  Returns:
      int: Current Unix epoch time
  """
  return int(datetime.now().strftime('%s'))


def currentUTC():
  """Returns current UTC time

  Returns:
      str: Current UTC time
  """
  return str(datetime.utcnow())


def filePathToFileName(path):
  """Get the filename (without extension) from a file path

  Args:
      path (str): path to file, e.g. "/path/to/file/filename.ext"

  Returns:
      str: file name of the path, e.g. "filename"
  """
  return os.path.splitext(os.path.basename(path))[0]

def outputFilename(name="", ext="", time=True):
  """Returns a date & time before the file name,
     e.g. outputFilename("file","ext",True)
     returns: YYYY-MM-DD__HH-MM-SS_file.ext

  Args:
      name (str, optional): name of the file. Defaults to "".
      ext (str, optional): file extension. Defaults to "".
      time (bool, optional): whether or not to include the time. Defaults to True.

  Returns:
      str: the filename
  """
  # get the date in the format specifed
  dateTime = datetime.now()
  dateTimeFormat = "%Y-%m-%d__%H-%M-%S" if time else "%Y-%m-%d"
  fileName = dateTime.strftime(dateTimeFormat)

  # construct the filename
  fileName = fileName + "_" + name if fileName != "" else fileName
  ext = "." + ext if ext != "" else ""

  return fileName + ext


def nestedDictValues(d):
  """Returns the values from a (nested) dict (in key alphabetical order)

  Args:
      d (dict): Dict with some values in it

  Yields:
      <Iterable>: Iterable of all the values
  """
  for key in sorted(d.keys()):
    if isinstance(d[key], dict):
      yield from nestedDictValues(d[key])
    else:
      yield d[key]


def nestedDictKeys(d):
  """Returns the keys from a (nested) dict (in key alphabetical order)

  Args:
      d (dict): Dict with some keys in it

  Yields:
      <Iterable>: Iterable of all the keys
  """
  for key in sorted(d.keys()):
    if isinstance(d[key], dict):
      yield from nestedDictKeys(d[key])
    else:
      yield key


def dictValuesToCSV(d):
  """Convert the values of a dict to comma separated values

  Args:
      d (dict): dict to be converted

  Returns:
      str: String of comma separated values
  """
  return ",".join([str(val) for val in nestedDictValues(d)])


def dictKeysToCSV(d):
  """Convert the keys of a dict to comma separated values

  Args:
      d (dict): dict to be converted

  Returns:
      str: String of comma separated keys
  """
  return ",".join([str(val) for val in nestedDictKeys(d)])