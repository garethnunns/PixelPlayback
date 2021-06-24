from datetime import datetime
import os
from threading import Timer

def currentTimestamp():
  return int(datetime.now().strftime('%s'))


def currentUTC():
  return str(datetime.utcnow())


def filePathToFileName(path):
  return os.path.splitext(os.path.basename(path))[0]


def outputFilename(name="", ext="", time=True):
  dateTime = datetime.now()
  dateTimeFormat = "%Y-%m-%d__%H-%M-%S" if time else "%Y-%m-%d"
  fileName = dateTime.strftime(dateTimeFormat)

  fileName = fileName + "_" + name if fileName != "" else fileName
  ext = "." + ext if ext != "" else ""

  return fileName + ext


class SetInterval(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)


def nestedDictValues(d):
  for v in sorted(d.keys()):
    if isinstance(d[v], dict):
      yield from nestedDictValues(d[v])
    else:
      yield d[v]


def dictValuesToCSV(d):
  return ",".join([str(v) for v in nestedDictValues(d)])


def nestedDictKeys(d):
  for v in sorted(d.keys()):
    if isinstance(d[v], dict):
      yield from nestedDictKeys(d[v])
    else:
      yield v


def dictKeysToCSV(d):
  return ",".join([str(v) for v in nestedDictKeys(d)])