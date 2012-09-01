'''
Created on 28-Aug-2012

@author: harsh
'''

from __future__ import division
import bottle
import logging 
from common.serverconfig import ServerConfig
from webapp.helper_functions import webrequest, wrap_links, auth
from common.decorators import get_url, track_data, wrap_exp


def get_user(environ):
    return environ.get('REMOTE_USER', 'unknown')

@wrap_exp()
@bottle.route("/index",method=['GET','POST'])
def index():
    return "Search Server is Running"

@wrap_exp()
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

@wrap_exp()
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

@wrap_exp()
@bottle.route('/admin',method='GET')
@bottle.auth_basic(auth)
@bottle.view("../../templates/admin")
def admin():
    '''
    Takes path from the route and tells Apache to server the file.
    
    @param path: The path to the file relative to root.
    @type path: str
    '''    
    return dict(user_data=ServerConfig.get_user_data(), site_data=ServerConfig.get_site_data())

@wrap_exp()
@bottle.route('/admin/getsitedata/:url#.*#',method='GET')
@bottle.auth_basic(auth)
def sitedata(url=None):
    '''
    Takes path from the route and tells Apache to server the file.
    
    @param path: The path to the file relative to root.
    @type path: str
    '''
    confirm, site_data = ServerConfig.get_site_data(url)
    if confirm:
        ret = site_data
        return dict(url=confirm, site_data = ret)
    else:
        ret = []
        for key, val in site_data.iteritems():
            ret.append( { key : len(val) })
        return dict(site_data = ret)

@wrap_exp()
@bottle.route('/admin/getuserdata/:user#.*#',method='GET')
@bottle.auth_basic(auth)
def userdata(user=None):
    '''
    Takes path from the route and tells Apache to server the file.
    
    @param path: The path to the file relative to root.
    @type path: str
    '''    
    confirm, user_data = ServerConfig.get_user_data(user)
    
    if confirm:
        ret = {}
        for key, val in user_data.iteritems():
            ret[key] = len(val)
        return dict(user = confirm, user_data = ret)
    else:
        ret = user_data.keys()
        return dict(user_data = ret)

def get_application(**kargs):
    '''
    Takes configuration params for creating middleware app. 
    @return: middleware app
    '''

    ServerConfig.initialize(app=bottle.default_app(), **kargs)
    logging.debug('Main Web Service Started')

    return ServerConfig.get_application()
