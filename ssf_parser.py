import regex as re


class ssfparser:

    def __init__(self, filename):
        with open(filename, 'r') as file:
            self.data = file.read()

    def fs_func(self, fs):
        fs_parts, fs_map = re.findall(' ([^\s>]*\=[^\s>]*)', fs), {}
        for part in fs_parts:
            pair = part.split('=')
            fs_map[pair[0]] = pair[1]
        return fs_map

    def lines_func(self, lines):
        parsed, wholes = {}, []
        for line in lines:
            try:
                line = line.split('\t')
                number, word, tag, fs_part = line[0], line[1], line[2], line[3]
                fs = self.fs_func(fs_part)
                parsed[number] = {'word': word, 'tag': tag, 'fs': fs}
                wholes.append(number)
            except:
                pass
        return parsed, wholes

    def reverse_dict(self, mapping):
        keys, reversed_mapping = list(mapping.keys()), {}
        keys.reverse()
        for key in keys:
            reversed_mapping[key] = mapping[key]
        return reversed_mapping

    def parse(self):
        data = re.sub('\t+', '\t', self.data)
        lines = data.split('\n')

        parsed, wholes = self.lines_func(lines)
        tmp, decimals = {}, []
        self.parser = {'data': {}}
        wholes.reverse()
        nodes = []
        for key in wholes:
            if '.' in key:
                decimals.append(key)
                tmp[key] = parsed[key]
            else:
                nodes.append(key)
                decimals.reverse()
                tmp = self.reverse_dict(tmp)
                self.parser[key] = tmp
                self.parser[key]['children'] = decimals
                tmp, decimals = {}, []
        nodes.reverse()
        self.parser = self.reverse_dict(self.parser)
        self.parser['nodes'] = nodes
        return self.parser
