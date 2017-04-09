#!/usr/bin/env python

# Main script , provides a beautiful/userfriendly name for executing our ap. Also it has main().
from utility_cls import Utility
from parser_cls import Parser

logger = Utility.rsynclog.logger_init('main')

def main():
    Utility.rsynclog.info_log(logger, '\n###Rsyncer.py start.###')
    data_dict = (Parser.main())
    response_list = Utility.rsync_all(data_dict)
    Utility.print_responses(response_list)


main()