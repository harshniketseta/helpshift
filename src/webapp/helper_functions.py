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
import bottle

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
            with cls.lock:
                cls.DB[name] = ConfigObj(os.path.join(value["basedir"], name))
    
    @classmethod
    def get_application(cls):
        return cls.app
    
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
    with open(os.path.join('/tmp/serverconfig.log'),'a') as fp:
        print >> fp ,"Inside Logging"+ os.path.abspath(os.path.join(os.path.curdir, d['handlers']['file']['filename']))
    dictConfig(d)
    logging.debug('Logger config updated')

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
