'''
Created on 01-Sep-2012

@author: harsh
'''
import logging
from logging.config import dictConfig
import beaker.middleware as bkmw
import beaker.cache as bkcache
import beaker.util as bkutil

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
