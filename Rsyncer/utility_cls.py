""" Utility.
Contains useful for programming functions. All it's methods is static and were used during the development process.
Have 3 sections:
1. Common utilities.
Contains useful during development methods.
2. Rsync Logger.
Logs the data in 'rsyncer.log' file during application work.
3. Helper.
User friendly purposes. Contains usage, help and other helpful for user messages. 
"""
import os
from subprocess import Popen, PIPE


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
    def subprocess_cmd(command):
        exec_cmd = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        out_msg, err_msg = exec_cmd.communicate()
        exitcode = exec_cmd.returncode
        return (out_msg, err_msg, exitcode)
      
    @staticmethod
    def rsync_all(data_dict):
        """Executes rsync command for each Client(Remote_request class) object"""
        response_list = list()
        for item in Utility.gen(data_dict['client']):
            response = item.rsync_cmd_dozens(data_dict['keys'], data_dict['host_files'])
            response_list.append(response)
            
        return response_list

    @staticmethod
    def print_responses(response_list):
        """Prints all the outcomes for rsync operation."""
        logger = Utility.rsynclog.logger_init('print_response')
        for index, item in enumerate(Utility.gen(response_list)):
            print (item)
            Utility.rsynclog.debug_log(logger, item)

    @staticmethod
    def pexpert_import(imp_err):
        logger = Utility.rsynclog.logger_init('import pexpect')
        positive_answer = ['y', 'ye', 'yo', 'yes', 'yeah', 'yourmum']  # Don't even ask...
        question_msg = "This application requires a \'pexpect\' module.\n" \
                       "Do you want to install it for your default python version?"
        warning_msg = "Warning: You must have a PIP package manager preinstalled on your OS to do that.\nAnswer: "
        answer = str(raw_input(question_msg + ' [yes(y)/no(n)]\n' + warning_msg)).lower()
        if (answer in positive_answer):
            try:
                print ('Installing \'pexpect\'module for your python. Sudo password might be required.')
                pexpect_install_cmd = 'sudo python -m pip install pexpect'.split(' ')
                out, err, exitcode = Utility.subprocess_cmd(pexpect_install_cmd)
            except:
                print err
                print ('Installation error: cannot load \'pexpect\' module for your python.')
                Utility.rsynclog.info_log(logger, 'Installation error: cannot load \'pexpect\' module for your python.')
                exit(1)
        else:
            print ('See you later!')
            exit(0)

    @staticmethod
    def print_msg(logger, some_str):
        print (some_str)
        Utility.rsynclog.info_log(logger, some_str)

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
            try:
                os.mkdir('/tmp/Rsyncer/')
            except:
                pass
            handler = logging.FileHandler('/tmp/Rsyncer/rsyncer.log'))
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
            """Universal error message.
                Allows u to post messages in both Debug and Info level of logger
                and exit program if needed.
                """
            print ('\n### {} :<').format(info_msg)
            if (info_msg):
                Utility.rsynclog.info_log(logger, info_msg)
            if (err_msg):
                Utility.rsynclog.debug_log(logger, err_msg)
            Utility.helper.usage_help()
            if (exitcode):
                exit(1)
