import sys
import time
import requests
import json


class WindowsOSSUpload:

    def __init__(self, filename=None, ip=None, port=None):
        self.ip = ip
        self.port = port
        self.url = None
        self.filename = filename

    def winUpload(self):
        timestr = str(int(time.time()))
        objectfile = sys.argv[1]
        file = objectfile.split("\\")[-1]
        filename = ".".join(file.split(".")[:-1]) + "_" + timestr + "." + file.split(".")[-1]
        self.filename = self.filename or filename
        self.url = "http://{}:{}/oss_upload?filename={}".format(self.ip, self.port, self.filename)
        files = {'objectfile': (filename, open(objectfile, 'rb'), 'application/octet-stream')}
        res = requests.post(url=self.url, files=files)
        rest = json.loads(res.text)
        print(rest['link'])
        input()  # 用于cmd窗口停留


if __name__ == '__main__':

    ip = "xxx.xxx.xxx.xxx"
    port = "xxxx"
    WindowsOSSUpload(ip=ip, port=port).winUpload()



