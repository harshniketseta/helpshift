'''
Created on 28-Aug-2012

@author: harsh
'''
import bottle
import sys
import os

FILE = os.path.abspath(__file__) if not hasattr(sys, 'frozen') else os.path.abspath(sys.executable)  
DIR = os.path.dirname(FILE)
PROJ_DIR = os.path.abspath(DIR + os.sep + '..')  # assumes we are 1 level deeper than the project root
sys.path.append(PROJ_DIR)  if not hasattr(sys, 'frozen') else sys.path.append(DIR)
os.chdir(DIR) # change to curr dir (relative to this file)

from webapp.mainserver import get_application
from common import singleton

application = get_application(**singleton.get_config_files(file_path=FILE, proj_dir=PROJ_DIR))

if __name__ == "__main__":
    bottle.run(app=application, host="localhost", port=9050)