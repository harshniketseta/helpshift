'''
Created on 28-Aug-2012

@author: harsh
'''
import os
from validate import Validator
from configobj import ConfigObj
from logging.config import dictConfig
import logging
from optparse import OptionParser
import threading
import beaker.middleware as bkmw
import beaker.cache as bkcache
import beaker.util as bkutil
import urllib2
from contextlib import closing
import json
import bottle
import random

class ServerConfig:
    
    def __init__(self):
        pass
    
    @classmethod
    def initialize(cls, app, basedir, configfile, configspecfile):
        
        cls.lock = threading.RLock()
        cls.basedir = basedir
        cls.DB = {}
        cls.app = app
        
        val = Validator()
        
        config = ConfigObj(os.path.join(cls.basedir, configfile))
        configspec = ConfigObj(os.path.join(cls.basedir, configspecfile), list_values=False, _inspec=True)
                    
        configuration = ConfigObj(config, configspec=configspec)     #Making new object out of merged config and configspec

        config_test = configuration.validate(val, preserve_errors=True)
    
        if config_test != True:
            with open(os.path.join(basedir,'logs/serverconfig.log'),'a') as fp:
                print >> fp ,'Configuration validation failed on',configfile,'and result is',config_test
        
        cls.config = configuration
        logger_config_update(cls.config['Logging'].dict())
        cls.app, cls.cache = beaker_config_update(cls.app, cls.config['Session'].dict(), cls.config['Caching'].dict())
        cls.create_data_dump()
        
        if config_test != True:
            logging.warning('Configuration validation not completely successful for %s and result is %s',configfile,config_test)
        logging.debug('Configuration validation successful for %s',configfile)
    
    @classmethod
    def get_config(cls):
        return cls.config
    
    @classmethod
    def create_data_dump(cls):
        for name, value in cls.config["DB"].iteritems():
            db_name = name+".db"
            spec_name = name+"_dbspec"
            with cls.lock:
                cls.DB[name] = ConfigObj(infile=os.path.join(value["basedir"], db_name), configspec=os.path.join(value["basedir"], spec_name))
                config_test = cls.DB[name].validate(Validator(), preserve_errors=True)
    
    @classmethod
    def get_application(cls):
        return cls.app
    
    @classmethod
    def get_cache(cls):
        return cls.cache
    
    @classmethod
    def update_user_data(cls, user, url, op):
        user_data = cls.DB["user_data"].get(user, {})
        if op == "inc":
            with cls.lock:
                user_data[url] = user_data.get(url, 0) + 1
                cls.DB["user_data"][user] = user_data
        with cls.lock:
            cls.DB["user_data"].write()
    
    @classmethod
    def update_site_data(cls, url, op):
        if op == "inc":
            with cls.lock:
                cls.DB["site_data"][url] = cls.DB["site_data"].get(url, 0) + 1
        
        with cls.lock:
            cls.DB["site_data"].write()
            
    @classmethod
    def get_user_data(cls):
        return cls.DB["user_data"]
    
    @classmethod
    def get_site_data(cls):
        return cls.DB["site_data"]

def get_config_files(file_path, proj_dir):
    '''
    Generic get-application method.
    Makes a application instance from the file_path and proj_dir passed.
    Expects that this is called from a meta_<appname>.py module. Expects that the main module
    is in <appname>.py and that the configuration files for the server are
    <appname>.ini and <appname>_config.ini available in the conf director.
    @param file_path: Path to the file being run.
    @type file_path: str
    
    @param proj_dir: Path where the project resides
    @type proj_dir: str
    
    @return: An an application instance returned by the main application module's get_application method
    '''
    file_dir = os.path.dirname(file_path)
    base_dir = os.path.abspath(proj_dir + os.sep + '..') 
    
    stem = os.path.splitext(os.path.basename(file_path))[0]
    module_name = stem.replace('meta_', '')
    conf_file = module_name + '.ini'
    conf_spec_file = module_name + '_configspec.ini'
    conf_dir = 'conf'

    return dict(basedir=base_dir, configfile=conf_dir + '/' + conf_file, configspecfile=conf_dir + '/' + conf_spec_file)

def logger_config_update(d):
    '''
    Called by Config to update the logging Configuration.
    '''
    
    d['formatters']['detailed']['format']='%(levelname)s:%(asctime)s:[%(process)d:%(thread)d]:%(funcName)s: %(message)s'
    dictConfig(d)
    logging.debug('Logger config updated')

def beaker_config_update(app, d1, d2):
    '''
    Called by Config to update the Cache Configuration.
    '''
    app = bkmw.SessionMiddleware(app, d1)
    cache = bkcache.CacheManager(**bkutil.parse_cache_config_options(d2))
    logger = logging.getLogger()
    logger.debug('Beaker config updated')
    return app, cache
    
def getparser(defhost='localhost', defport=8080):
    '''
    @summary: Returns the dict object which holds the parsed values from the command line arg.
    
    @param defhost: The default hostname to be used (defaults to localhost)
    @type defhost: str
    
    @param defport: The default port to be used (defaults to 8080)
    @type defport: int
    
    @return: dict  
    '''
    usage="usage: %prog [options]"
    parser = OptionParser(usage=usage, version="0.1")
    parser.add_option("-i", "--host", dest="host", default=defhost,\
                      help="hostname or ip address. (default: localhost)")
    parser.add_option("-p", "--port", dest="port", default=defport, \
                      help="port number (default 8080)")
    return parser

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
    logging.debug("In wrap_links")
    data = json.loads(response['data'])
    logging.debug("data:%s",type(data))
    try:
        response['data'] = recursive_wrap(data)
    except Exception as e:
        logging.exception("Exception in wrap_links:%s",e)
    return response

def recursive_wrap(data):
    if isinstance(data, dict):
        for key, value in data.iteritems():
            data[key] = run_replacer(value) if key in ServerConfig.get_config()["Search"]["link_fields"] else recursive_wrap(value)  
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
        return val.replace(ServerConfig.get_config()["Search"]["match_pattern"], ServerConfig.get_config()["Search"]["wrapping_link"])
    
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
                ServerConfig.update_site_data(url, "inc")
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

def auth(user, password):
    logging.debug("user=%s, password=%s", user, password)
    if user == 'admin' and password == "harsh":
        return True
    return False
    