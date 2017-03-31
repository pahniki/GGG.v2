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
    def port_to_keys(keys_list, port):
        """ Add '-p port' to a -e params, if port exist """
        if (port):
            index = 0
            key_str = '-e \'ssh -p {}\''.format(port)
            for item in Utility.gen(keys_list):
                if (item.startswith('-e')):
                    index = keys_list.index(item)
                    keys_list[index] = key_str
                    break
            if (not index):
                keys_list.append(key_str)

        return keys_list

    @staticmethod
    def rsync_all(data_dict):
        for item in Utility.gen(data_dict['client']):
            keys = list()
            keys.extend(data_dict['keys'])

            item.pinger()
            keys = Utility.port_to_keys(keys, item.port)
            item.rsync_cmd(keys, data_dict['host_files'])

            #########################Logger section#########################

    class rsynclog:
        '''
            Custom logger to store all rsync wrapper actions.
        '''

        @staticmethod
        def logger_init(some_str):
            ''' Initialise new logger '''
            import logging
            logger = logging.getLogger(some_str)
            logger.setLevel(logging.INFO)
            logger.setLevel(logging.DEBUG)
            handler = logging.FileHandler('rsyncer.log')
            formatter = logging.Formatter('[%(asctime)s] - %(name)11s - %(levelname)6s : %(message)s',datefmt='%d-%m-%y %H:%M')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            return logger

        @staticmethod
        def info_log(logger, infostr):
            ''' Log info message '''
            logger.info(infostr)

        @staticmethod
        def debug_log(logger, infostr):
            ''' Log debug message '''
            logger.debug(infostr)

