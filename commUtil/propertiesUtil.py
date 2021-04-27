# -*- coding: utf-8 -*-


class Properties:

    def __init__(self, file_name):
        self.file_name = file_name
        self.properties = {}

    def __getdict(self, str_name, dict_name, value):
        """

        :param str_name:
        :param dict_name:
        :param value:
        :return:
        """
        if str_name.find('.') > 0:
            k = str_name.split('.')[0]
            dict_name.setdefault(k, {})
            return self.__getdict(str_name[len(k) + 1:], dict_name[k], value)
        else:
            dict_name[str_name] = value
            return

    def getproperties(self):
        try:
            pro_file = open(self.file_name, 'Ur')
            for line in pro_file.readlines():
                line = line.strip().replace('\n', '')
                if line.find("#") != -1:
                    line = line[0:line.find('#')]
                if line.find('=') > 0:
                    strs = line.split('=')
                    strs[1] = line[len(strs[0]) + 1:]
                    self.__getdict(strs[0].strip(), self.properties, strs[1].strip())
        except Exception as e:
            raise e
        else:
            pro_file.close()
        return self.properties


if __name__ == '__main__':
    p = Properties("../login/config.properties")
    properties_map = p.getproperties()
    print(properties_map)
    print(properties_map.get('Aliexpress').get('username'))
