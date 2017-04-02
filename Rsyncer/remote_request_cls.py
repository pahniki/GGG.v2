import subprocess
import os
import socket
import time
from utility_cls import Utility

logger = Utility.rsynclog.logger_init('remote_request_cls')

class Remote_request():
    """ Produces objects for each remotehost machine """
    ind = 0
    inst_array = list()

    def __init__(self, hostname, password, try_hostrequest_parse):
        """Constructor"""
        data_dict = try_hostrequest_parse(hostname)
        self.username = data_dict['username']
        self.adress = data_dict['ip']
        self.port = data_dict['port']
        self.rem_dir = data_dict['remote_dir']
        self.password = password
        self.ind = Remote_request.ind
        Remote_request.ind += 1
        self.full_adress = (self.username + '@' + self.adress + ':' + self.rem_dir)

    def rsync_cmd_deco_deco(DEBUG):
        """ Decorator for DEBUG purposes. 
            Hides 'subprocess' work result and print rsync cmd if True. """

        def resync_cmd_deco(func):
            if (DEBUG == True):
                def wrapper(self, keys, files):
                    print ('rsync -r ' + ' '.join(keys) + ' ' + ' '.join(files) + ' ' + self.full_adress
                           + '  -pass=' + self.password)
                    res_obj = Response(0)
                    print res_obj

                return wrapper
            else:
                return func

        return resync_cmd_deco

    def self_print(self):
        print (('###Request object number {}.\n'
                'Attributes:\n'
                '   username: {}\n'
                '   remote adress: {}\n'
                '   remote dir: {}\n'
                '   password: {}\n'
                '   port: {}').format(Remote_request.ind, self.username, self.adress, self.rem_dir, self.password,
                                      self.port))

    def checker(self):
        """check if directory exist and create it if so"""
        dir_check = os.system("ssh {0}@{1} '[ -d {2} ]'".format(self.username, self.adress, self.remote_dir))
        if not dir_check:
            os.system("ssh {0}@{1} 'mkdir {2}'".format(self.username, self.adress, self.remote_dir))

    def pinger(self):
        """Check connection to remote machine and ssh enable for chosen port"""
        ping_check = subprocess.Popen(['ping','-c1',self.adress],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        out,err = ping_check.communicate()
        exitcode=ping_check.returncode

        # ping_check = os.system("ping -c1 {}".format(self.adress))
        if not exitcode:
            print("Host {} is alive!".format(self.adress))
            s = socket.socket()
            if (not self.port):
                port = 22
            else:
                port = self.port
            try:
                s.bind((self.adress, port))
            except:
                print("SSH is enabled on host {}".format(self.adress))
            else:
                print("Host {} is not available by SSH".format(self.adress))
                exit(1)
        else:
            print("Host {} is dead!".format(self.adress))
            exit(1)

    def passwordless_con(self):
        pass

    def try_rsync_cmd(self,keys,files):
        """ try-except for rsync_cmd function """
        try:
            return self.rsync_cmd(keys,files)
        except:
            Utility.helper.error_msg(logger,'\'rsync\' command error','\'rsync\' command could not execute.')

    @rsync_cmd_deco_deco(DEBUG=False)
    def rsync_cmd(self, keys, files):
        """Execute rsync command"""
        rsync_cmd = subprocess.Popen(['rsync', '-r'] + keys + files + [self.full_adress, ],
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = rsync_cmd.communicate()
        exitcode = rsync_cmd.returncode

        print out
        
        return Response(exitcode, out, err)


class Response:
    index = 0

    def __init__(self, exitcode, out='', err=''):
        self.name = 'ro.{}-{}'.format(str(int(time.time())), str(Response.index))
        Response.index += 1

        self.exitcode = exitcode
        self.out = out
        self.err = err

    @property
    def is_success(self):
        return (not self.exitcode and not self.err and not 'exit' in self.out.lower())

    def __repr__(self):
        return ('{} Success: {}'.format(self.name, str(self.is_success)))
