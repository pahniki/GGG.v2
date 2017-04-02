import re
from inputparser import Inputparser
from utility_cls import Utility
from remote_request_cls import Remote_request

logger = Utility.rsynclog.logger_init('parser_cls')


class Parser(Inputparser):
    """Second stage parser. Parsing unknown for 'argparse' parameters 
        and splits 'username:port@hostname:/dir' into pieces. """

    @staticmethod
    def keys_parse(input_list):
        """ Fill the key_list with parameters for rsync. """
        SINGLE_PARAM = tuple('PavSzqi')
        key_set = set()

        for item in Utility.gen(input_list):
            if (item.startswith('-')):
                if (all(ch in SINGLE_PARAM for ch in Utility.gen(item[1:]))):
                    key_set.update([('-' + char) for char in item[1:]])

        return (list(key_set))

    @staticmethod
    def try_hostrequest_parse(hostname):
        """Catches exception during hostrequest_parse"""
        try:
            return Parser.hostrequest_parse(hostname)
        except:
            Utility.helper.error_msg(logger, hostname, 'Incorrect remote request form!')

    @staticmethod
    def hostrequest_parse(hostname):
        """ username:port@ip_address:/dir parsing """
        delim_ind = re.search("[.,:@]", hostname)
        username = hostname[:delim_ind.start()]
        port = ''
        if (hostname[delim_ind.start()] is not '@'):
            hostname = hostname[delim_ind.end():]
            delim_ind = re.search("[.,:@]", hostname)
            port = hostname[: delim_ind.start()]
        if (username == 'root'):
            remote_dir = '//root'
        else:
            remote_dir = '/home/' + username
        if (':/' in hostname):
            id_end = hostname.rfind(':')
            remote_dir += hostname[id_end + 1:]
        else:
            id_end = len(hostname)

        host_id = hostname[delim_ind.end():id_end]

        data_dict_host = {'remote_dir': remote_dir,
                          'username': username, 'ip': host_id,
                          'port': port}

        return data_dict_host

    @staticmethod
    def find_hostrequest(some_lis):
        """  """
        if (not len(some_lis)):
            Utility.helper.error_msg(logger, some_lis, 'No File/directories or \'username@hostname:/dir\' parameter:')

        host_dict = Parser.form_dict(some_lis)

        return host_dict

    @staticmethod
    def form_dict(hostrequest):
        """ Form a { remoterequest : password } dictionary from a list """
        if (len(hostrequest) > 1):
            host_dict = dict()
            pass_len = len('-pass=')
            for index, item in enumerate(Utility.gen(hostrequest)):
                if (index + 1 < len(hostrequest)):
                    next_item = hostrequest[index + 1]
                if (not item.startswith('-pass=')):
                    if next_item.startswith('-pass='):
                        host_dict.update({item: next_item[pass_len:]})
                    else:
                        host_dict.update({item: ''})
        else:
            host_dict = {hostrequest[0]: ''}

        Utility.rsynclog.info_log(logger, 'Host dictionary.')
        Utility.rsynclog.debug_log(logger, host_dict)
        return host_dict

    @staticmethod
    def fill_in_clients(data_dict, hostnamedict):
        data_dict.update({'client': []})
        for key, item in hostnamedict.iteritems():
            data_dict['client'].append(Remote_request(key, item, Parser.try_hostrequest_parse))

        return data_dict

    @staticmethod
    def main():
        """ Head method of the Parser class. Calls all contained methods to modify and parse input data.
            :returns dict """
        data_dict, unknownlist = Parser.inputparse()
        hostnamedict = Parser.find_hostrequest(data_dict['hosts'])
        data_dict['keys'] += Parser.keys_parse(unknownlist)
        Parser.fill_in_clients(data_dict, hostnamedict)

        Utility.rsynclog.debug_log(logger, data_dict)

        return data_dict
