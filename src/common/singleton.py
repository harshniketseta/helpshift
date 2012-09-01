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
    Generic get-config method.
    Makes a configuration dictionary from the file_path and proj_dir passed.
    Expects that this is called from a meta_<appname>.py module. Expects that the main module
    is in <appname>.py and that the configuration files for the server are
    <appname>.ini and <appname>_configspec.ini available in the conf director.
    
    @param file_path: Path to the file being run.
    @type file_path: str
    
    @param proj_dir: Path where the project resides
    @type proj_dir: str
    
    @return: A configuration dictionary.
    '''
    file_dir = os.path.dirname(file_path)
    base_dir = os.path.abspath(proj_dir + os.sep + '..') 
    
    stem = os.path.splitext(os.path.basename(file_path))[0]
    module_name = stem.replace('meta_', '')
    conf_file = module_name + '.ini'
    conf_spec_file = module_name + '_configspec.ini'
    conf_dir = 'conf'

    return dict(basedir=base_dir, configfile=conf_dir + '/' + conf_file, configspecfile=conf_dir + '/' + conf_spec_file)


class Server:
    '''
    A object used as a singleton to load the server's configuration and provide us with helpful functions on the server level.
    
    '''
    
    @classmethod
    def initialize(cls, app, basedir, configfile, configspecfile):
        '''
        Sets up the ServerConfig instance.
        
        Loads the configuration.
        Runs validation checks on it.
        Loads up individual modules which are relying on the config.
        
        
        @param app: WSGI App
        @type app: WSGI Middleware App
        
        @param basedir: The basedir of the project.All file path information is relative to basedir
        @type basedir: str
         
        @param configfile: The relative path to the file holding the config.
        @type configfile: str
         
        @param configspecfile: The relative path to the file holding validation information for the config.
        @type configspecfile: str
        '''
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
        cls.read_database()
        
        if config_test != True:
            logging.warning('Configuration validation not completely successful for %s and result is %s',configfile,config_test)
        logging.debug('Configuration validation successful for %s',configfile)
    
    @classmethod
    @property
    def siteDB(cls, collection_name):
        '''
        Returns the handler to the MongoDB Collections object for site_data.
        '''
        connection = Connection(cls.config["MongoDB"]["host"], cls.config["MongoDB"]["port"])
        db = connection[cls.config["MongoDB"]["db_name"]]
        return db[cls.config["MongoDB"]["site_db"]["collection_name"]]
    
    @classmethod
    @property
    def userDB(cls, collection_name):
        '''
        Returns the handler to the MongoDB Collections object for user_data.
        '''
        connection = Connection(cls.config["MongoDB"]["host"], cls.config["MongoDB"]["port"])
        db = connection[cls.config["MongoDB"]["db_name"]]
        return db[cls.config["MongoDB"]["user_db"]["collection_name"]]
    
    @classmethod
    def get_config(cls):
        '''
        @return: The server configuration. 
        '''
        return cls.config
    
    @classmethod
    def read_database(cls):
        '''
        Reads the db files.
        
        Saves the handlers to provide access at a later poiint of time.
        '''
        for name, value in cls.config["FileDB"].iteritems():
            db_name = name+".db"
            spec_name = name+"_dbspec"
            with cls.lock:
                cls.FileDB[name] = ConfigObj(infile=os.path.join(value["basedir"], db_name), configspec=os.path.join(value["basedir"], spec_name))
                config_test = cls.FileDB[name].validate(Validator(), preserve_errors=True)
                if config_test != True:
                    logging.warning("Something went wrong in reading the DB:%s.Errors:%s", name, config_test)
    
    @classmethod
    def get_application(cls):
        '''
        @return: Returns the app.
        '''
        return cls.app
    
    @classmethod
    def get_cache(cls):
        '''
        @return: Returns the CacheManager Object.
        '''
        return cls.cache
    
    @classmethod
    def update_user_data(cls, user, url, op):
        '''
        A handler which updates the database with the data provided.
        
        As this problem statement requires only a limited DB manipulations this is a good way to help debug issues.
        
        @param user: Unique Identifier for a spcified user in this case, the IP Address of the user.
        @type user: str
        
        @param url: The a unique click made on a link for the following URL. 
        @type url: str
        
        @param op: The operation to be performed on the DB with this data.
        @type op: str
        '''
        user_data = cls.FileDB["user_data"].get(user, {})
        if op == "inc": #TODO:Maybe it should take a function.And handler can call that function with the lock.That way this part of the code is abstracted.
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
        '''
        A handler which updates the database with the data provided.
        
        As this problem statement requires only a limited DB manipulations this is a good way to help debug issues.
        
        @param user: Unique Identifier for a spcified user in this case, the IP Address of the user.
        @type user: str
        
        @param url: The a unique click made on a link for the following URL. 
        @type url: str
        
        @param op: The operation to be performed on the DB with this data.
        @type op: str
        '''
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
        '''
        Returns the user data from the handler.If user is specified and exists in the user_data DB return data of only of the specified user.
        
        @param user: Unique Identifier for a spcified user in this case, the IP Address of the user.
        @type user: str

        @return: Section if user exists otherwise returns the ConfigObj. 
        '''
        try:
            return user, cls.FileDB["user_data"][user]
        except KeyError:
            return None, cls.FileDB["user_data"]
    
    @classmethod
    def get_site_data(cls, url=None):
        '''
        Returns the site data from the handler.If url is specified and exists in the site_data DB return data of only of the specified url.
        
        @param url: A URL.
        @type url: str

        @return: Section if url exists otherwise returns the ConfigObj. 
        '''
        try:
            return url, cls.FileDB["site_data"][url]
        except:
            return None, cls.FileDB["site_data"]

