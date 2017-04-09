"""
Remote request class. 
Stores the data for each separate remote host.
Contains a must have methods to provide a comfortable execution for 'rsync' command.
Response class.
Used to create an objects as work out results for several functions.
"""
import time
import os
from utility_cls import Utility

# pexpect import
try:
    import pexpect
except ImportError as imp_err:
    Utility.pexpert_import(imp_err)

logger = Utility.rsynclog.logger_init('remote_request_cls')

# pexpect import
try:
    import pexpect
except ImportError as imp_err:
    Utility.pexpert_import(imp_err)

logger = Utility.rsynclog.logger_init('remote_request_cls')

        
class Remote_request():
    """ Produces objects for each remote host machine """
    ind = 0
    inst_array = list()

    def __init__(self, hostname, password, try_hostrequest_parse):
        """Constructor"""
        data_dict = try_hostrequest_parse(hostname)
        self.username = data_dict['username']
        self.adress = data_dict['ip']
        self.port = data_dict['port']
        self.rem_dir = data_dict['remote_dir']
        self.__password = password
        self.ind = Remote_request.ind
        Remote_request.ind += 1
        self.short_adress = self.username + '@' + self.adress
        self.full_adress = (self.username + '@' + self.adress + ':' + self.rem_dir)

    def rsync_cmd_deco_deco(DEBUG):
        """ Decorator for DEBUG purposes. 
            Hides 'subprocess' work result and print rsync cmd if True. """

        def resync_cmd_deco(func):
            if (DEBUG == True):
                def wrapper(self, keys, files):
                    Utility.print_msg(logger,
                                      'rsync -r ' + ' '.join(keys) + ' ' + ' '.join(files) + ' ' + self.full_adress
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
                '   port: {}').format(Remote_request.ind, self.username, self.adress, self.rem_dir, self.__password,
                                      self.port))

    def dir_checker(self, username, ip, remote_dir):
        """check if directory exist and create it if so"""
        Utility.print_msg(logger,'Checking if directory exist,' \
                          'password could be required for that.')
        dir_check_cmd = ['ssh', '{}@{}'.format(username, ip), '[', '-d', remote_dir, ']']
        out, err, exitcode = Utility.subprocess_cmd(dir_check_cmd)
        if (exitcode):
            Utility.print_msg(logger,'Creating remote dirrectory.')
            dir_maker_cmd = ['ssh', '{}@{}'.format(username, ip), 'mkdir', remote_dir]
            out, err, exitcode = Utility.subprocess_cmd(dir_maker_cmd)
            if (not exitcode):
                Utility.print_msg(logger, "Directory {} was created for host {}".format(remote_dir, ip))
        else:
            Utility.print_msg(logger, "Directory {} exists for host {}".format(remote_dir, ip))
        if (err):
            Utility.print_msg(logger, err)

            return Response(self.short_adress, exitcode, out, err)

    def pinger(self):
        """Check connection to remote machine and ssh enable for chosen port"""
        ping_check_cmd = ['ping', '-c2', self.adress]
        out, err, exitcode = Utility.subprocess_cmd(ping_check_cmd)
        if not exitcode:
            Utility.print_msg(logger, "Host {} is alive!".format(self.adress))
        else:
            err = "Host {} is dead!".format(self.adress)
            Utility.print_msg(logger, err)
            return Response(self.short_adress, exitcode, out, err)

    def passwordless_con(self):
        """Provides passwordless ssh connection"""
        self.home_path = os.environ['HOME']

        def sshkeygen(short_adress):
            """Provides passwordless ssh connection"""
            Utility.print_msg(logger, 'using ssh-keygen to create a key')
            path = self.home_path + '/.ssh/id_rsa'
            sshkeygen_cmd = ['ssh-keygen', '-f', path, '-t', 'rsa', '-q', '-N', '']
            out, err, exitcode = Utility.subprocess_cmd(sshkeygen_cmd)
            print (exitcode, out)
            if ('error' in err.lower()):
                message = ('\nError: ' + err.split('\n', 1)[0])
                Utility.helper.error_msg(logger, err, 'ssh-keygen', exitcode=0)
                return Response(self.short_adress, exitcode, err=message)

        def ssh_copy_id(short_adress, password=''):
            try:
                path = self.home_path + '/.ssh/id_rsa.pub'
                child = pexpect.spawn('ssh-copy-id -i ' + path + ' ' + short_adress)
                child.expect('password:', timeout=20)
                child.sendline(password)
                child.interact()                

            except RuntimeError as runtime_err:
                Utility.helper.error_msg(logger, runtime_err, 'ssh-copy-id Runtime error', exitcode=0)
                return Response(self.short_adress, 1, err='ssh-copy-id error')
            except pexpect.EOF as eof_err:
                pass


        response = sshkeygen(self.short_adress)
        if (not response):
            response = ssh_copy_id(self.short_adress, self.__password)
        return response

    def port_to_keys(self, keys_list, port):
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

    def with_password(self):
        """Checks if password exist"""
        if (self.__password):
            return self.passwordless_con()

    def rsync_cmd_dozens(self, keys_list, files):
        """Collaborate rsync and all advanced methods."""
        keys = list()
        keys.extend(keys_list)
        keys = self.port_to_keys(keys, self.port)
        # Execute commands untill an error occur.
        response = self.pinger()
        if (not response):
            response = self.with_password()
            if (not response):
                response = self.dir_checker(self.username, self.adress, self.rem_dir)
                if (not response):
                    response = self.try_rsync_cmd(keys, files)
        return response

    def try_rsync_cmd(self, keys, files):
        """ try-except for rsync_cmd function """
        try:
            return self.rsync_cmd(keys, files)
        except:
            Utility.helper.error_msg(logger, '\'rsync\' command error', '\'rsync\' command could not execute.',
                                     exitcode=0)
            return Response(self.short_adress, 1, err='rsync execution error')

    @rsync_cmd_deco_deco(DEBUG=False)
    def rsync_cmd(self, keys, files):
        """Execute rsync command"""
        rsync_cmd = ['rsync', '-r'] + keys + files + [self.full_adress, ]
        out, err, exitcode = Utility.subprocess_cmd(rsync_cmd)
        Utility.print_msg(logger, out)
        return Response(self.short_adress, exitcode, out, err)


class Response:
    """Response class to create Objects as a result of work for several functions"""
    index = 0

    def __init__(self, remote_host, exitcode, out='', err=''):
        """ Response constructor """
        self.name = 'ro.{}-{}'.format(str(int(time.time())), str(Response.index))  # Unique id for each object
        Response.index += 1
        self.remote_host = remote_host
        self.exitcode = exitcode
        self.out = out
        self.err = err

    @property
    def is_success(self):
        """ Is response successful """
        return (not self.exitcode and not self.err and not 'exit' in self.out.lower())

    def __repr__(self):
        """Show recorded information"""
        message = 'Response to {}. Success : {}'.format(self.remote_host, str(self.is_success))
        if (self.err):
            message += ('\nError: ' + self.err.split('\n', 1)[0])
        return message
