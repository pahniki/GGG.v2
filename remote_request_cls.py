import subprocess
import os
import socket


class Remote_request_cls():
    """ Produces objects for each remotehost machine """
    ind = 0
    inst_array = list()

    def __init__(self, data_dict):
        """Constructor"""
        self.username = data_dict['username']
        self.adress = data_dict['ip']
        self.port = data_dict['port']
        self.rem_dir = data_dict['remote_dir']
        self.password = data_dict['password']
        self.ind = Remote_request_cls.ind
        Remote_request_cls.ind += 1
        self.full_adress = (self.username + '@' + self.adress + ':' + self.rem_dir)

    def self_print(self):
        print (('###Request object number {}.\n'
                'Attributes:\n'
                '   username: {}\n'
                '   remote adress: {}\n'
                '   remote dir: {}\n'
                '   password: {}\n'
                '   port: {}').format(Remote_request_cls.ind, self.username, self.adress, self.rem_dir, self.password,
                                      self.port))

    def checker(self):
        """check if directory exist and create it if so"""
        dir_check = os.system("ssh {0}@{1} '[ -d {2} ]'".format(self.username, self.adress, self.remote_dir))
        if not dir_check:
            os.system("ssh {0}@{1} 'mkdir {2}'".format(self.username, self.adress, self.remote_dir))

    def pinger(self):
        """Check connection to remote machine and ssh enable for chosen port"""
        ping_check = os.system("ping -c3 {}".format(self.adress))
        if not ping_check:
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

    def rsync_cmd(self, keys, files):
        """Execute rsync command"""
        rsync_cmd = subprocess.Popen(['rsync', '-r'] + keys + files + [self.full_adress, ],
                                     stdout=subprocess.PIPE,stderr = subprocess.PIPE)
        out, err = rsync_cmd.communicate()
        print out
        print err

    @classmethod
    def self_create(cls, data_dict):
        Remote_request_cls.inst_array.append(Remote_request_cls(data_dict))
