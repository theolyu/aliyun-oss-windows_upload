[toc]

---

**完整项目代码见[GitHub](https://github.com/theolyu/aliyun-oss-windows_upload)**
**本项目教程见[CSDN博客](https://blog.csdn.net/ForeverLyu/article/details/90083024)**

---

### 阿里云OSS
#### 阿里云OSS选择
- 阿里云： 0-5GB(含)部分 免费 只限香港地区
- 新建Bucket时, 所属区域选香港

#### 阿里云OSS API使用
- [阿里云OSS API官方参考](https://help.aliyun.com/document_detail/31947.html?spm=a2c4g.11186623.6.1096.187166f2KoWnQt)
- OSS通过使用AccessKeyId/ AccessKeySecret对称加密的方法来验证某个请求的发送者身份
- 建议使用RAM账户AccessKey：RAM账户由阿里云账号授权生成，所拥有的AccessKey拥有对特定资源限定的操作权限
- 根据官方文档封装阿里云OSS API
    - 安装Python SDK: `pip install oss2`
    - 最高仅支持Python3.5
```
import oss2
import time


class RunOSS:
    def __init__(self, AccessKeyId=None, AccessKeySecret=None, Endpoint=None, BuckerName=None, filename=None):
        self.AccessKeyId = AccessKeyId
        self.AccessKeySecret = AccessKeySecret
        self.Endpoint = Endpoint  # Endpoint(香港, 其他地区根据实际情况修改): 'http://oss-cn-hongkong.aliyuncs.com'
        self.BuckerName = BuckerName
        self.filename = filename or str(int(time.time()))

    def getBucket(self):
        auth = oss2.Auth(self.AccessKeyId, self.AccessKeySecret)
        bucket = oss2.Bucket(auth, self.Endpoint, self.BuckerName)
        return bucket

    def uploadFIle(self, objectfile, isFile=True):
        bucket = self.getBucket()
        if isinstance(objectfile, str):
            objectname = self.filename+'.'+objectfile.split('.')[-1]
        else:
            objectname = self.filename
        try:
            if isFile:
                with open(objectfile, mode='rb') as f:
                    ret = bucket.put_object(objectname, f)
            else:
                ret = bucket.put_object(objectname, objectfile)
            link = "http://{}.oss-cn-hongkong.aliyuncs.com/".format(self.BuckerName) + objectname
            return {'status': ret.status, 'link': link}
        except Exception as e:
            return e
    
    ...
```

### 使用Flask封装API实现本地图片上传
#### 代码
```
import json
from flask import Flask, request, jsonify, Response
from aliyunOSSRun import RunOSS

# Flask对象
app = Flask(__name__)

def response_headers(content):
    resp = Response(content)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/oss_upload/', methods=['POST'])
def upload_oss_file():
    if request.files.get('objectfile'):
        objectfile = request.files['objectfile']
        filename = str(request.args.get('filename', ""))
        ret = RunOSS(filename=filename).uploadFIle(objectfile=objectfile, isFile=False)
        print(ret[key] for key in ret)
        return jsonify(ret)
    else:
        content = json.dumps({"error_code": "1001"})
        resp = response_headers(content)
        return resp

if __name__ == '__main__':
    app.run(debug=False, port=5000, host='0.0.0.0')   # 启动服务
```

> 可以在阿里云服务器上后台开启该任务, 用于接收OSS上传任务

#### Flask Bug
- 高并发报错: 
```
requests.exceptions.ConnectionError: ('Connection aborted.', BrokenPipeError(32, 'Broken pipe'))
```
- 解决方案:
> 使用Flask+gevent异步WEB架构解决
代码修改如下:
```
import json

from flask import Flask, request, jsonify, Response
from gevent import pywsgi
from gevent import monkey

from aliyunOSSRun import RunOSS

monkey.patch_all()
# Flask对象
app = Flask(__name__)

        ...

if __name__ == '__main__':

    port = 5000
    server = pywsgi.WSGIServer(('0.0.0.0', port), app)
    server.serve_forever()
```

### Windows右键实现一键上传文件并返回文件OSS路径
#### 编写Python脚本获取文件路径, 并上传至阿里云Flask接口
```
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
```

> 其中`sys.argv[1]`用于读取cmd中传递的参数, 该处是获取待上传文件的路径
> 最后加input(), 防止cmd窗口自动关闭

#### 增加右键任务按钮
- `Win + R`打开命令行, 输入`regedit`打开注册表
- 找到`HKEY_CLASSES_ROOT\*\shell`目录, 新建`name`项, 命名即为右键显示的任务名称
- 进入`name`项目录, 新建`command`项
- 进入`command`项目录, 新建一个`字符串值`
- 输入值: `D:\Anaconda3\envs\pyenv35\python D:\OSSRun\winOSSUpload.py %1`
    - 其中前者为python路径, 后者为项目文件路径
    - 在注册表的指定打开方式路径后加上（空格）%1, 表示系统向其传递的文件路径

---

### 参考
- [解决博客图片存储——阿里云的OSS运用](https://segmentfault.com/a/1190000009263202)
- [Flask+gevent 异步 WEB 架构](https://blog.csdn.net/feng020a/article/details/60343804)
- [怎样把自己的程序添加到系统右键并获得调用该程序的文件地址及文件名](https://bbs.csdn.net/topics/380061058)
- [如何给注册表添加右键菜单](https://www.cnblogs.com/cheungxiongwei/p/7541447.html)
- [cmd怎么往python中传参数](https://zhidao.baidu.com/question/552219304949359292.html)
