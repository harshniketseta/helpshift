'''
Created on 28-Aug-2012

@author: harsh
'''

import logging
import urllib2
from contextlib import closing
import json

from common.singleton import Server
import datetime

def webrequest(url):
    '''
    Makes GET requests.
    Parses to JSON before returning the response.
    '''
    try:
        request = urllib2.Request(url=url)
        with closing(urllib2.urlopen(request)) as req:
            return dict(status="success", data=json.loads(req.read()))
    except urllib2.HTTPError as err:
        logging.exception('HTTPError: %d', err.code)
        return dict(status="HTTPError", data=err.code)
    except urllib2.URLError as err:
        logging.exception('URLError: %s', err.reason)
        return dict(status="URLError", data=err.reason)

def wrap_links(response):       
    '''
    Function accepts reponse from the webreqest function.
    '''
    logging.debug("Request for wrapping links")
    data = response['data']
    try:
        response['data'] = recursive_wrap(data)
    except Exception as e:
        logging.exception("Exception in wrap_links:%s",e)
    logging.debug("Returning wrap links")
    return response

def recursive_wrap(data):
    '''
    Recursively goes through the whole structure(dict or list), searching for the keys specified in link_fields in the config.
    If found calls run_replacer.
    
    If data is neither list nor dict returns the data.
    '''
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
    '''
    If list given calls run_replacer on each element of string.
    
    If string replaces the match_pattern given in config with wrapping_links given in config.
    
    Otherwise calls recursive_wrap if it is a list of dict.
    '''
    if isinstance(val, list):
        new_val = map(run_replacer, val)
        return new_val
    elif isinstance(val, str) or isinstance(val, unicode):
        val = val.replace(Server.get_config()["Search"]["match_pattern"], Server.get_config()["Search"]["replace_with"])
        return Server.get_config()["Search"]["wrapping_link"] + val
    else:
        return recursive_wrap(val)
    
def auth(user, password):
    '''
    Basic Auth function.
    '''
    if user == 'admin' and password == "helpshift":
        logging.debug("user %s authenticated", user)
        return True
    return False

def value_sort(x,y):
    '''
    Function for cmp in sort.
    Sorts according to the first value in the dict.
    Thus in our case sorts according to count.
    <---higher--------------to------------------lower--->
    '''
    return y.values()[0] - x.values()[0]

def time_sort(x,y):
    '''
    Function for cmp in sort.
    Sorts according to the date and time in values.
    <---latest--------------to------------------farthest--->
    
    
    Extracting date and time from string.
    Extracting year, month, day from date and parsing it to int
    Extracting hour, minute, second from time and parsing it to int
    Creating datetime.datetime objects
    This is done twice, once for x and once for y
    
    Subtracting to create deltatime object.
    Returning deltatime in seconds parsed to int, as cmp only takes int return.
    '''
    x_datetime = datetime.datetime(*(str_to_date(x.values()[0].split("'")[1])+str_to_time(x.values()[0].split("'")[3])))
    y_datetime = datetime.datetime(*(str_to_date(y.values()[0].split("'")[1])+str_to_time(y.values()[0].split("'")[3])))    
    delta = y_datetime - x_datetime     
    return int(delta.total_seconds())

def url_time_sort(x,y):
    '''
    Function for cmp in sort.
    Sorts according to the date and time in values.
    <---latest--------------to------------------farthest--->
    
    Extracting date and time from string.
    Extracting year, month, day from date and parsing it to int
    Extracting hour, minute, second from time and parsing it to int
    Creating datetime.datetime objects
    This is done twice, once for x and once for y
    
    Subtracting to create deltatime object.
    Returning deltatime in seconds parsed to int, as cmp only takes int return.
    '''
    delta = datetime.datetime(*(str_to_date(y.split("'")[3])+str_to_time(y.split("'")[5]))) - datetime.datetime(*(str_to_date(x.split("'")[3])+str_to_time(x.split("'")[5])))     
    return int(delta.total_seconds())
        
def str_to_date(str_date):
    '''
    @param str_date: date
    @type str_date: str
    
    @return: year, month, day as int
    '''
    return int(str_date.split('/')[2]), int(str_date.split('/')[1]), int(str_date.split('/')[0])

def str_to_time(str_time):
    '''
    @param str_time: time
    @type str_time: str
    
    @return: hour, minutes, seconds as int
    '''
    str_time, str_p = str_time.split(' ')
    return int(str_time.split(':')[0]) + ( 12 if str_p == "PM" else 0 ), int(str_time.split(':')[1]), int(str_time.split(':')[2])