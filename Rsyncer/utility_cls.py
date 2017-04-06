# utility
import os


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
            key_str = '-e ssh -p {}'.format(port)
            for item in Utility.gen(keys_list):
                if (item.startswith('-e')):
                    index = keys_list.index(item)
                    keys_list[index] = key_str
                    break
            if (not index):
                keys_list.insert(0, key_str)

        return keys_list

    @staticmethod
    def rsync_all(data_dict):
        response_list = list()
        for item in Utility.gen(data_dict['client']):
            keys = list()
            keys.extend(data_dict['keys'])

            connection_error = item.pinger()
            if (not connection_error):
                keys = Utility.port_to_keys(keys, item.port)
                response = item.try_rsync_cmd(keys, data_dict['host_files'])
                response_list.append(response)
            else:
                response_list.append(connection_error)

        return response_list

    @staticmethod
    def print_responses(response_list):
        logger = Utility.rsynclog.logger_init('print_response')
        for index, item in enumerate(Utility.gen(response_list)):
            print (item)
            Utility.rsynclog.debug_log(logger,item)

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
            formatter = logging.Formatter('[%(asctime)s] - %(name)11s - %(levelname)6s : %(message)s',
                                          datefmt='%d-%m-%y %H:%M')
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
            #########################Helper section#########################

    class helper:
        '''Helper object will raise help messages'''

        @staticmethod
        def usage_help():
            print('\n   usage:   '
                  'rsyncer.py [/dir file1 file2][-process][-e ssh][username:port@ip:/destination [-pass=PASS]][-PavSzq]\n\n'
                  'Runs rsync application with input parameters. For more info use "rsyncer.py -h".\n')

        @staticmethod
        def main_help():
            Utility.helper.usage_help()
            print('All available keys:\n'
                  '-process                    If exists raise -process flag for rsync\n'
                  '-pass=[Password]            Password for connection to remote host\n'
                  '-e [connection type]        Connection type ssh or rsh\n'
                  '-P                          Analog rsync --partial --progress\n'
                  '-a                          Archive mode\n'
                  '-v                          Verbose input\n'
                  '-S                          Parse argument files\n'
                  '-z                          Compress data stream\n'
                  '-q                          Quiet input\n'

                  'Single remoute host can be entered without [...] brackets.\n'
                  'Multiple remoute hosts should be entered as list in [...] brackets.\n '
                  '\n'
                  '!!After [ and before ] brackets spaces are  necessary!!\n'
                  '\n'
                  'Example: \n'
                  'rsyncer.py -Pa /dir file1 [ username1@remote1 -pass=123 username2@remote2 username3@remote3 -pass=qwe ]\n'
                  'Valid separators between username and port are: comma, spot, colon (,.:)\n'
                  'Examples: rsyncer.py /usr root@host\n'
                  '          rsyncer.py /usr/wildcard* file3.avi root,22@hostname:/junk')

        @staticmethod
        def error_msg(logger, err_msg, info_msg='', exitcode=1):
            print ('\n### {} :<').format(info_msg)
            if (info_msg):
                Utility.rsynclog.info_log(logger, info_msg)
            if (err_msg):
                Utility.rsynclog.debug_log(logger, err_msg)
            Utility.helper.usage_help()
            if (exitcode):
                exit(1)

        @staticmethod
        def connection_type_help():
            print('Something goes wrong. Try -e ssh, -e rsh or use help.')

        @staticmethod
        def multiple_host_help():
            print('Something goes wrong. Spaces are  necessary after open and before closed brackets.\n'
                  'For more information use help\n'
                  'Example: [ username1@remote1 -pass=123 username2@remote2 username3@remote3 -pass=qwe ]')

        @staticmethod
        def random_help():
            print('Oops, something goes wrong. Try to use help.')
