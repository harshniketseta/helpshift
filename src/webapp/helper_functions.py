'''
Created on 28-Aug-2012

@author: harsh
'''

import logging
import urllib2
from contextlib import closing
import json

from common.singleton import Server

def webrequest(url):
    try:
        request = urllib2.Request(url=url)
        with closing(urllib2.urlopen(request)) as req:
            return dict(status="success", data=req.read())
    except urllib2.HTTPError as err:
        logging.exception('HTTPError: %d', err.code)
        return dict(status="HTTPError", data=err.code)
    except urllib2.URLError as err:
        logging.exception('URLError: %s', err.reason)
        return dict(status="URLError", data=err.reason)

def wrap_links(response):       
    '''
    At the moment wrapping links according to DuckDuckGo structure. 
    '''
    logging.debug("Request for wrapping links")
    data = json.loads(response['data'])
    try:
        response['data'] = recursive_wrap(data)
    except Exception as e:
        logging.exception("Exception in wrap_links:%s",e)
    logging.debug("Returning wrapp links")
    return response

def recursive_wrap(data):
    if isinstance(data, dict):
        for key, value in data.iteritems():
            data[key] = run_replacer(value) if key in Server.get_config()["Search"]["link_fields"] else recursive_wrap(value)  
        return data
    elif isinstance(data, list):
        new_data = map(recursive_wrap, data)
        return new_data
    else:
        return data
        
def run_replacer(val):
    if isinstance(val, list):
        new_val = map(run_replacer, val)
        return new_val
    else:
        return val.replace(Server.get_config()["Search"]["match_pattern"], Server.get_config()["Search"]["wrapping_link"])
    
def auth(user, password):
    
    if user == 'admin' and password == "helpshift":
        logging.debug("user %s authenticated", user)
        return True
    return False

def value_sort(x,y):
    return y.values()[0] - x.values()[0]
    