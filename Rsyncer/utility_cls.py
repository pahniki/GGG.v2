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


class rsynclog:

    ''' Initialise new logger '''
    @staticmethod
    def logger_init(some_str):
        import logging
        logger = logging.getLogger(some_str)
        logger.setLevel(logging.INFO)
        logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler('rsyncer.log')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    ''' Log info message '''
    @staticmethod
    def info_log(logger, infostr):
        logger.info(infostr)

    ''' Log debug message '''

    @staticmethod
    def debug_log(logger, infostr):
        logger.debug(infostr)
