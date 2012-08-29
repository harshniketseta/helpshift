'''
Created on 28-Aug-2012

@author: harsh
'''

from __future__ import division
import bottle
import os, sys
import logging
import urllib2
from contextlib import closing



FILE = os.path.abspath(__file__) if not hasattr(sys, 'frozen') else os.path.abspath(sys.executable)  
DIR = os.path.dirname(FILE)
PROJ_DIR = os.path.abspath(DIR + os.sep + '..')  # assumes we are 1 level deeper than the project root
sys.path.append(PROJ_DIR)  if not hasattr(sys, 'frozen') else sys.path.append(DIR)
os.chdir(DIR) # change to curr dir (relative to this file) 

from webapp import helper_functions
from webapp.helper_functions import ServerConfig

if __name__ == "__main__":
# being called standalone
    prefix = '/main'
    template_prefix = ''
else:
    prefix = ''
    template_prefix = ''

def get_user(environ):
    return environ.get('REMOTE_USER', 'unknown')

@bottle.route(prefix+"/index",method=['GET','POST'])
def index():
    return "Search Server is Running, Config=" + ServerConfig.get_config().dict()

@bottle.route(prefix+'/search/:query#.*#',method=['GET','POST'])
def search(query):
    '''
    Takes path from the route and tells Apache to server the file.
    
    @param path: The path to the file relative to root.
    @type path: str
    '''
    try:
        request = urllib2.Request(url='http://api.duckduckgo.com/?q='+query+'&format=json&pretty=1')
        with closing(urllib2.urlopen(request)) as req:
            return dict(status="success", data=req.read())
    except urllib2.HTTPError as err:
        logging.exception('HTTPError: %d', err.code)
        return dict(status="HTTPError", data=err.code)
    except urllib2.URLError as err:
        logging.exception('URLError: %s', err.reason)
        return dict(status="URLError", data=err.reason)

def get_application(**kargs):
    '''
    Takes configuration params for creating middleware app. 
    @return: middleware app
    '''
    
    ServerConfig.initialize(app=bottle.default_app(), **kargs)
    with open(os.path.join('/tmp/serverconfig.log'),'a') as fp:
        print >> fp ,str(ServerConfig.get_config().dict())+"kargs"+str(kargs)
    logger = logging.getLogger('SPARX.MainServer')
    logger.debug('Main Web Service Started')

    return ServerConfig.get_application()

if __name__ == '__main__':
    
    parser=helper_functions.getparser(defhost='localhost',defport=9050)
    opt, args = parser.parse_args(sys.argv[1:])

    bottle.debug(True)
    app = helper_functions.get_application(**helper_functions.get_config_files(file_path=FILE, proj_dir=PROJ_DIR))
    bottle.run(app=app, host=opt.host, port=opt.port)
