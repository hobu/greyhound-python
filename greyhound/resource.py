
import numpy as np
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

import json
import struct

from . import box

class Resource(object):

    def __init__(self, server, name):
        self.server = server
        self.name = name
        self.info = self.get_info()

    def get_url(self):
        url = self.server.url+"resource/"+self.name
        return url

    url = property(get_url)

    def get_info(self, data=None):

        def buildNumpyDescription(schema):
            output = {}
            formats = []
            names = []
            for s in schema:
                t = s['type']
                if t == 'floating':
                    t = 'f'
                elif t == 'unsigned':
                    t = 'u'
                else:
                    t = 'i'

                f = '%s%d' % (t, int(s['size']))
                names.append(s['name'])
                formats.append(f)
            output['formats'] = formats
            output['names'] = names
            return output

        if not data:
            command = self.url + "/info"
            u = urlopen(command)
            data = u.read()
        j = json.loads(data)
        j['dtype'] = buildNumpyDescription(j['schema'])

        return j


    def read(self, bounds, depthBegin, depthEnd, compress=False):
        import lazperf
        import json
        import numpy as np

        compressed = 'false'
        if compress:
            compressed = 'true'
        command = self.url + '/read?'
        command += 'bounds=%s&depthEnd=%d&depthBegin=%d&compress=%s' % (bounds.url, depthEnd, depthBegin, compressed)
        u = urlopen(command)
        data = u.read()

        # last four bytes are the point count
        count = struct.unpack('<L',data[-4:])[0]

        if compress:
            arr = np.frombuffer(data[:-4], dtype=np.uint8)
            schema = self.info['schema']
            s = json.dumps(schema)
            dt = lazperf.buildNumpyDescription(s)
            d = lazperf.Decompressor(arr, s)
            output = np.zeros(count * dt.itemsize, dtype=np.uint8)
            decompressed = d.decompress(output)
            array = np.ndarray(shape=(count,),buffer=decompressed,dtype=dt)
        else:

            array = np.ndarray(shape=(count,),buffer=data,dtype=self.info['dtype'])
        return array


