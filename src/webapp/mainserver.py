'''
Created on 28-Aug-2012

@author: harsh
'''

from __future__ import division
import bottle
import os, sys
import logging

FILE = os.path.abspath(__file__) if not hasattr(sys, 'frozen') else os.path.abspath(sys.executable)  
DIR = os.path.dirname(FILE)
PROJ_DIR = os.path.abspath(DIR + os.sep + '..')  # assumes we are 1 level deeper than the project root
sys.path.append(PROJ_DIR)  if not hasattr(sys, 'frozen') else sys.path.append(DIR)
os.chdir(DIR) # change to curr dir (relative to this file) 

from webapp import helper_functions
from webapp.helper_functions import ServerConfig, webrequest, wrap_links,\
    get_url, track_data, auth

def get_user(environ):
    return environ.get('REMOTE_USER', 'unknown')

@bottle.route("/index",method=['GET','POST'])
def index():
    return "Search Server is Running"

@bottle.route('/search/:query#.*#',method=['GET','POST'])
def search(query):
    '''
    Takes query and returns wraped results.
    
    @param query: The query to search.
    @type query: str
    
    @return: Wrapped Results.
    '''
    logging.debug("Query:%s",query)
    @ServerConfig.cache.cache(expire=3600)
    def do_search(query):
        logging.debug("Fetching query from DuckDuckGo API")
        return wrap_links(webrequest(url='http://api.duckduckgo.com/?q='+query+'&format=json&pretty=1'))
    return do_search(query)

@bottle.route('/link',method='GET')
@get_url()
@track_data()
def link(url):
    '''
    Takes path from the route and tells Apache to server the file.
    
    @param path: The path to the file relative to root.
    @type path: str
    '''    
    bottle.redirect(url)

@bottle.route('/admin',method='GET')
@bottle.auth_basic(auth)
def admin():
    '''
    Takes path from the route and tells Apache to server the file.
    
    @param path: The path to the file relative to root.
    @type path: str
    '''    
    return dict(user_data=ServerConfig.get_user_data(), site_data=ServerConfig.get_site_data())

def get_application(**kargs):
    '''
    Takes configuration params for creating middleware app. 
    @return: middleware app
    '''

    ServerConfig.initialize(app=bottle.default_app(), **kargs)
    logging.debug('Main Web Service Started')

    return ServerConfig.get_application()

if __name__ == '__main__':
    
    parser=helper_functions.getparser(defhost='localhost',defport=9050)
    opt, args = parser.parse_args(sys.argv[1:])

    bottle.debug(True)
    app = get_application(**helper_functions.get_config_files(file_path=FILE, proj_dir=PROJ_DIR))
    bottle.run(app=app, host=opt.host, port=opt.port)
