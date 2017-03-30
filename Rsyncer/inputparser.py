'''
PyAuthomation training task: Rsync wrapper.Stage 1: Argparse.
Takes known parameters from CLI input. Returns output_dict.
All keys stored in output_dict['keys'].
All recognised files,dirrectories to copy and remote dirrectory is
stored in output_dict['host_files']
Password to remote host located in output_dict['password']
'''
import argparse
import rsync_logger


class Inputparser:
    """ First stage parser. Using 'argparse' module to pull out all valid parameters."""
    @staticmethod
    def inputparse():
        """ Static method which draws out all valid parameters. Based on 'argparse' module. Returns dict,list """
        output_dict = {}
        single_param = tuple('PavSzqih')
        parser = argparse.ArgumentParser(add_help=False)
        filesgarbage = []
        unknownkeys = []
        keys = []
        parser.add_argument('-process', action="store_true", default=False)
        parser.add_argument('-pass', action="store", dest="userpass", type=str)
        parser.add_argument('-e', action="store", dest='connection', type=str)
        parser.add_argument('files', type=str, help='list of files and dirrs to copy', nargs='*')
        known, unknown = parser.parse_known_args(['-PavSzqi','-process','-pass=noOneLiveForever','-h','/dir','some','file','[root:port@hostname:/not\ dir another@hostname:/dir andone@more:/dir]'])
        # Fill arguments in group
        unknown = set(unknown)
        for i in unknown:
            if i[1:] in single_param:
                    keys.append(i)
            else:
                unknownkeys.append(i)
        for i in known.files:
            filesgarbage.append(i)
        if known.connection == 'ssh':
            print(known.connection)
            keys.append('-e ssh')
        elif known.connection == 'rsh':
            keys.append('-e rsh')
        if known.process:
            keys.append('-process')
        output_dict.update({'host_files': filesgarbage, 'keys': keys, 'password': known.userpass})
        rsync_logger.customlogger.info_log(rsync_logger.customlogger(), "Input parser output: {}".format(output_dict))
        return output_dict, unknownkeys


