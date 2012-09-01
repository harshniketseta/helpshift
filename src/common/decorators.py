'''
Created on 01-Sep-2012

@author: harsh
'''
import logging
import random
import bottle
from bottle import HTTPResponse
from common.singleton import Server

def get_url():
    '''
    Extracts the URL from GET.
    Does the correct replacements.
    And calls the func with the url.
    '''
    def decorator(func):
        def wrapper(*args, **kargs):
            url = bottle.request.GET.get('url', '#') #@UndefinedVariable
            logging.debug("URL:%s",url)
            url = url.replace(Server.get_config()["Search"]["replace_with"], Server.get_config()["Search"]["match_pattern"])
            return func(*args, url=url, **kargs)
        return wrapper
    return decorator

def track_data():
    '''
    Extracts the users IP Address.
    Requests to update data.Depending upon the life the cache, the request may or may not be accepted.
    '''
    def decorator(func):
        def wrapper(*args, **kargs):

            @Server.cache.cache()
            def update_data(user, url):
                Server.update_user_data(user, url, "inc")
                Server.update_site_data(user, url, "inc")
                logging.debug("Unique click detected.New data entry made.")
                return random.randint(1, 10000)
                
            user = bottle.request.environ.get("REMOTE_ADDR", None) #@UndefinedVariable
            logging.debug("User:%s",user)
            url = kargs.get("url",None)
            if user and url:
                feed_back = update_data(user, url)
                if feed_back:
                    logging.debug("Data Record id=%s", feed_back)
                    
            return func(*args, **kargs)
        return wrapper
    return decorator

def wrap_exp():
    '''
    '''
    def decorator(func):
        def wrapper(*args, **kargs):
            try:
                logging.debug("Calling function with args=%s, kargs=%s", args, kargs)
                return func(*args, **kargs)
            except HTTPResponse as e:
                raise e
            except Exception as e:
                logging.exception("Exception caught in wrap exception:%s",e)
        return wrapper
    return decorator
