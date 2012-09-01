'''
Created on 28-Aug-2012

@author: harsh
'''

from __future__ import division
import bottle
import logging 
from common.singleton import Server
from webapp.helper_functions import webrequest, wrap_links, auth, value_sort,\
    time_sort, url_time_sort
from common.decorators import get_url, track_data, wrap_exp

def get_user(environ):
    return environ.get('REMOTE_USER', 'unknown')


@bottle.route("/index",method='GET')
@wrap_exp()
def index():
    return "Search Server is Running"

@bottle.route('/search/:query#.*#',method='GET')
@wrap_exp()
def search(query):
    '''
    Takes query and returns wraped results.
    
    @param query: The query to search.
    @type query: str
    
    @return: Wrapped Results.
    '''
    logging.debug("Query Recieved:%s",query)
    @Server.cache.cache(expire=3600)
    def do_search(query):
        logging.debug("Query not in cache, Fetching from DuckDuckGo API")
        return wrap_links(webrequest(url='http://api.duckduckgo.com/?q='+query+'&format=json&pretty=1'))
    return do_search(query)

@bottle.route('/link',method='GET')
@wrap_exp()
@get_url()
@track_data()
def link(url):
    '''
    Takes path from the route and tells Apache to server the file.
    
    @param path: The path to the file relative to root.
    @type path: str
    '''
    logging.debug("Redirecting to URL:%s",url)    
    bottle.redirect(url)

@bottle.route('/admin',method='GET')
@bottle.auth_basic(auth)
@bottle.view("../../templates/admin")
@wrap_exp()
def admin():
    '''
    Takes path from the route and tells Apache to server the file.
    
    @param path: The path to the file relative to root.
    @type path: str
    '''
    
    return dict(user_data=Server.get_user_data(), site_data=Server.get_site_data())

@bottle.route('/admin/getsitedata/:url#.*#',method='GET')
@bottle.auth_basic(auth)
@wrap_exp()
def sitedata(url=None):
    '''
    Takes path from the route and tells Apache to server the file.
    
    @param path: The path to the file relative to root.
    @type path: str
    '''
    if url:
        url = url.replace('__slashslash__', '//')
    logging.debug("URL Recieved: %s", url)
    confirm, site_data = Server.get_site_data(url)
    logging.debug("confirm: %s,site_data: %s", confirm, site_data)
    if confirm:
        ret = site_data
        ret.sort(cmp=url_time_sort)
        return dict(url=confirm, site_data = ret)
    else:
        ret = []
        for key, val in site_data.iteritems():
            ret.append( { key : len(val) })
            ret.sort(cmp=value_sort)
        return dict(site_data = ret)

@bottle.route('/admin/getuserdata/:user#.*#',method='GET')
@bottle.auth_basic(auth)
@wrap_exp()
def userdata(user=None):
    '''
    Takes path from the route and tells Apache to server the file.
    
    @param path: The path to the file relative to root.
    @type path: str
    '''    
    confirm, user_data = Server.get_user_data(user)
    
    if confirm:
        ret = []
        for key, val in user_data.iteritems():
            for v in val:
                ret.append( { key : v })
            ret.sort(cmp=time_sort)
        return dict(user = confirm, user_data = ret)
    else:
        ret = user_data.keys()
        return dict(user_data = ret)

def get_application(**kargs):
    '''
    Takes configuration params for creating middleware app. 
    @return: middleware app
    '''

    Server.initialize(app=bottle.default_app(), **kargs)
    logging.debug('Main Web Service Started')
    return Server.get_application()
