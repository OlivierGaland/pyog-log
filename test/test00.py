# https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/
# https://packaging.python.org/en/latest/tutorials/packaging-projects/
#
# https://pypi.org/classifiers/
#
# build : python -m build
# upload :
# twine check dist/*

import sys
import os
cwd = os.getcwd()
sys.path.append('src')

from og_log import LOG,LEVEL

LOG.start()
LOG.level(LEVEL.debug)
LOG.debug("this is a debug log")
LOG.info("this is a info log")
LOG.warning("this is a warning log")
LOG.error("this is a error log")
LOG.fatal("this is a fatal log")
#LOG.temp("this is a temp log")
