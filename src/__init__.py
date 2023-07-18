"""The structure of this project consists of:

- -a **encoder.py** that is the core of the project
    - -Contains the main functionality
    - -imports and employs supportive modules or packages
- -a **utils** package that contains supportive functionality
- -an **about.py** that contains the project details

Project supports logging and a global logger is initialized in the main package.

Example of using logger
-----------------------
Import:
    .. highlight:: python
    .. code-block:: python

        from src import logger
Usage:
    .. highlight:: python
    .. code-block:: python

        logger.info("info message")
        logger.debug("debug message")
        logger.error("error message")

For all the logging messages look at:
    https://docs.python.org/3.8/howto/logging.html
"""

import os
import logging.config
import time


# Construct the paths based on the path that the execution starts from
basename = os.path.basename(os.getcwd())
rootdir = os.path.dirname(os.getcwd())
root = (
    rootdir
    if os.path.basename(rootdir) == "sentence-encoder"
    else os.path.dirname(rootdir)
)

logdir = os.path.join(os.getcwd(), "logs")
fname = os.path.join(os.getcwd(), "configs/logger.conf")


if not os.path.exists(logdir):
    os.makedirs(logdir)

logname = time.strftime("%m%d%Y-%H:%M:%S")

logging.config.fileConfig(
    fname=fname,
    disable_existing_loggers=False,
    defaults={"logfilename": f"{logdir}/{logname}.log"},
)
logger = logging.getLogger(__name__)
