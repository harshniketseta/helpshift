'''
Created on 01-Sep-2012

@author: harsh
'''
import os
import threading
from datetime import datetime
from configobj import ConfigObj
from validate import Validator
from optparse import OptionParser
import logging
from pymongo.connection import Connection
from common.configs import logger_config_update, beaker_config_update

    
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


class ServerConfig:
    
    def __init__(self):
        pass
    
    @classmethod
    def initialize(cls, app, basedir, configfile, configspecfile):
        
        cls.lock = threading.RLock()
        cls.basedir = basedir
        cls.FileDB = {}
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
    def DB(cls, collection_name):
        connection = Connection(cls.config["MongoDB"]["host"], cls.config["MongoDB"]["port"])
        return connection[collection_name]
    
    @classmethod
    def get_config(cls):
        return cls.config
    
    @classmethod
    def create_data_dump(cls):
        for name, value in cls.config["FileDB"].iteritems():
            db_name = name+".db"
            spec_name = name+"_dbspec"
            with cls.lock:
                cls.FileDB[name] = ConfigObj(infile=os.path.join(value["basedir"], db_name), configspec=os.path.join(value["basedir"], spec_name))
                config_test = cls.FileDB[name].validate(Validator(), preserve_errors=True)
    
    @classmethod
    def get_application(cls):
        return cls.app
    
    @classmethod
    def get_cache(cls):
        return cls.cache
    
    @classmethod
    def update_user_data(cls, user, url, op):
        user_data = cls.FileDB["user_data"].get(user, {})
        if op == "inc":
            now = datetime.now()
            new_data = user_data.get(url, [])
            new_data.append(("%s/%s/%s"%(now.day, now.month, now.year), now.strftime('%I:%M:%S %p')))
            with cls.lock:
                user_data[url] = new_data
                cls.FileDB["user_data"][user] = user_data
        with cls.lock:
            cls.FileDB["user_data"].write()
    
    @classmethod
    def update_site_data(cls, user, url, op):
        if op == "inc":
            now = datetime.now()
            new_data = cls.FileDB["site_data"].get(url, [])
            new_data.append([user, "%s/%s/%s"%(now.day, now.month, now.year), now.strftime('%I:%M:%S %p')])
            with cls.lock:
                cls.FileDB["site_data"][url] = new_data 
        with cls.lock:
            cls.FileDB["site_data"].write()
            
    @classmethod
    def get_user_data(cls, user=None):
        try:
            return user, cls.FileDB["user_data"][user]
        except KeyError:
            return None, cls.FileDB["user_data"]
    
    @classmethod
    def get_site_data(cls, url=None):
        try:
            return url, cls.FileDB["site_data"][url]
        except:
            return None, cls.FileDB["site_data"]

