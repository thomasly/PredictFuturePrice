import os
import logging
from datetime import datetime


def get_logger(loggerName, filePath=None, timeStamp=True):
  if filePath is None or timeStamp:
    time_stamp = datetime.strftime(datetime.now(), format=r"%Y%m%d_%H%M%S")
  if filePath is None:
    os.makedirs("log", exist_ok=True)
    filePath = os.path.join("log", "log")
  else:
    os.makedirs(os.path.dirname(filePath))

  if timeStamp:
    head, base = os.path.split(filePath)
    filename_tokens = base.split(".")
    if len(filename_tokens) > 1:
      filename_tokens[-2] += "_" + time_stamp
    else:
      filename_tokens[0] += "_" + time_stamp
    filePath = os.path.join(head, ".".join(filename_tokens))

  fl_handler = logging.FileHandler(filePath)
  fl_handler.setLevel(logging.DEBUG)
  st_handler = logging.StreamHandler()
  st_handler.setLevel(logging.INFO)

  fm = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
  fl_handler.setFormatter(fm)
  st_handler.setFormatter(fm)

  logger = logging.getLogger()
  # remove all the handlers that have been added to the default logger
  for h in logger.handlers:
    logger.removeHandler(h)
    
  logger.setLevel(logging.DEBUG)
  logger.addHandler(fl_handler)
  logger.addHandler(st_handler)

  return logger