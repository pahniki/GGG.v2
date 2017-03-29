# utility

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
    def rsync_all(data_dict):
        for item in Utility.gen(data_dict['client']):
            item.pinger()
            item.rsync_cmd(data_dict['keys'], data_dict['host_files'])