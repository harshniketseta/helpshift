'''
Created on 01-Sep-2012

@author: harsh
'''
import logging
from webapp.helper_functions import ServerConfig
import random
import bottle

def get_url():
    '''
    '''
    def decorator(func):
        def wrapper(*args, **kargs):
            url = bottle.request.GET.get('url', '#') #@UndefinedVariable
            logging.debug("URL:%s",url)
            url = url.replace('__slashslash__', '//')
            return func(*args, url=url, **kargs)
        return wrapper
    return decorator

def track_data():
    '''
    '''
    def decorator(func):
        def wrapper(*args, **kargs):

            @ServerConfig.cache.cache()
            def update_data(user, url):
                ServerConfig.update_user_data(user, url, "inc")
                ServerConfig.update_site_data(user, url, "inc")
                return random.randint(1, 10000)
                
            user = bottle.request.environ.get("REMOTE_ADDR", None) #@UndefinedVariable
            logging.debug("User:%s",user)
            url = kargs.get("url",None)
            if user and url:
                feed_back = update_data(user, url)
                if feed_back:
                    logging.debug("Data Recoded id=%s", feed_back)
            return func(*args, **kargs)
        return wrapper
    return decorator

def wrap_exp():
    '''
    '''
    def decorator(func):
        def wrapper(*args, **kargs):
            try:
                return func(*args, **kargs)
            except Exception as e:
                logging.exception("Exception caught in wrap_exp",e)
        return wrapper
    return decorator
