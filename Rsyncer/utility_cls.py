# utility

class Utility:
    @staticmethod
    def gen(it_obj):
        for item in it_obj:
            yield item

    @staticmethod
    def print_dict(some_dict):
        for key in Utility.gen(some_dict):
            print ('{} = {}'.format(key, some_dict[key]))

    @staticmethod
    def print_client(clientlist):
        for item in Utility.gen(clientlist):
            item.self_print()

    @staticmethod
    def rsync_all(data_dict):
        for item in Utility.gen(data_dict['client']):
            item.pinger()
            item.rsync_cmd(data_dict['keys'], data_dict['host_files'])



'''
Custom logger to store all rsync wrapper actions.
'''
class customlogger:

    ''' Initialise new logger '''
    def newlogger(self):
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