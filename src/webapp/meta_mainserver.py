'''
Created on 28-Aug-2012

@author: harsh
'''
import bottle

'''
Apache requires a file in source file (cannot deal with only .pyc). To enable this, we have created
a generic meta_<servername>.py file. If the conventions are followed, we just need to copy this file to the
appropriate name. 

The convention is as follows
For server named xyzserver.py
    meta filename should be meta_xyzserver.py
    configuration file should be xyzserver.ini

Our current assumption is that we are one level deep in the src folder of python project
    e.g. webapp/appserver.py
    
    
Currently we will require to create a copy of this file for each meta-server required. 
'''

import sys
import os

FILE = os.path.abspath(__file__) if not hasattr(sys, 'frozen') else os.path.abspath(sys.executable)  
DIR = os.path.dirname(FILE)
PROJ_DIR = os.path.abspath(DIR + os.sep + '..')  # assumes we are 1 level deeper than the project root
sys.path.append(PROJ_DIR)  if not hasattr(sys, 'frozen') else sys.path.append(DIR)

from webapp.mainserver import get_application
from webapp import helper_functions

application = get_application(**helper_functions.get_config_files(file_path=FILE, proj_dir=PROJ_DIR))

if __name__ == "__main__":
    bottle.run(app=application, host="localhost", port=9050)