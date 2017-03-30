'''
Custom logger to store all rsync wrapper actions.
'''


class customlogger(object):

    ''' Initialise new logger '''
    def __init__(self):
        import logging
        self.logger = logging.getLogger('rsyncer_logger')
        self.logger.setLevel(logging.INFO)
        self.logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler('rsyncer.log')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    ''' Log info message '''
    def info_log(self, infostr):
        self.logger.info(infostr)

    ''' Log debug message '''
    def debug_log(self, infostr):
        self.logger.debug(infostr)





