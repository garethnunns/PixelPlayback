from datetime import datetime
import os

def currentTimestamp():
  return int(datetime.now().strftime('%s'))

def filePathToFileName(path):
  return os.path.splitext(os.path.basename(path))[0]