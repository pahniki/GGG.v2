import re
from inputparser import Inputparser
from utility_cls import Utility
from remote_request_cls import Remote_request_cls


class Parser(Inputparser):
    """Second stage parser. Parsing unknown for 'argparse' parameters 
        and splits 'username:port@hostname:/dir' into pieces. """

    @staticmethod
    def keys_parse(input_list):
        """ fill the key_list with parameters for rsync. """
        SINGLE_PARAM = tuple('PavSzqi')
        key_set = set()

        for item in Utility.gen(input_list):
            if (item.startswith('-')):
                if (all(ch in SINGLE_PARAM for ch in Utility.gen(item[1:]))):
                    key_set.update([('-' + char) for char in item[1:]])

        return (list(key_set))

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
        if (':/' in hostname):
            id_end = hostname.rfind(':')
            remote_dir = '/home/'+username+ hostname[id_end + 1:]
        else:
            id_end = len(hostname)
            if(username == 'root'):
                remote_dir = '//root'
            else:
                remote_dir = '/home/' + username
        host_id = hostname[delim_ind.end():id_end]

        data_dict_host = {'remote_dir': remote_dir,
                          'username': username, 'ip': host_id,
                          'port': port}

        return data_dict_host

    @staticmethod
    def port_to_keys(keys_list, port):
        """ Add '-p port' to a -e params, if port exist """
        if (port):
            ind = 0
            key_str = '-e \'ssh -p {}\''.format(port)
            for item in Utility.gen(keys_list):
                if (item.startswith('-e')):
                    ind = keys_list.index(item)
                    keys_list[ind] = key_str
                    break
            if (not ind):
                keys_list.append(key_str)
            keys_list = keys_list

        return keys_list

    @staticmethod
    def find_hostrequest(some_lis):
        """ Looks for last non key item in list (without '-')
            saves it as class variable """
        if (len(some_lis) > 1):
            hostrequest = some_lis[-1]
        else:
            print ('No File/directories or \'username@hostname:/dir\' parameter')
            exit(1)
            hostrequest = ''

        some_lis.remove(hostrequest)
        return some_lis, hostrequest

    @staticmethod
    def main():
        """ Head method of the Parser class. Calls all contained methods to modify and parse input data.
            :returns dict """

        data_dict, unknownlist = Parser.inputparse()
        data_dict['host_files'], hostname = Parser.find_hostrequest(data_dict['host_files'])
        data_dict['keys'] += Parser.keys_parse(unknownlist)
        client_date_dict = (Parser.hostrequest_parse(hostname))
        data_dict['keys'] = (Parser.port_to_keys(data_dict['keys'], client_date_dict['port']))

        client_date_dict['password'] = data_dict['password']
        data_dict.pop('password')

        client = Remote_request_cls(client_date_dict)

        if (not data_dict.has_key('client')):
            data_dict.update({'client': []})
        data_dict['client'].append(client)

        return data_dict
