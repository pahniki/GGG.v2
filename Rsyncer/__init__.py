from parser_cls import Parser
from utility_cls import Utility

def main():
    data_dict = (Parser.main())
    response_list = Utility.rsync_all(data_dict)
    Utility.print_responses(response_list)
