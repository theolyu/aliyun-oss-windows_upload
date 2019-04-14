import oss2
import time


class RunOSS:
    def __init__(self, AccessKeyId=None, AccessKeySecret=None, Endpoint=None, BuckerName=None, filename=None):
        self.AccessKeyId = AccessKeyId
        self.AccessKeySecret = AccessKeySecret
        self.Endpoint = Endpoint
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

    def downloadFile(self, ObjectName, filepath=None, toFile=True):
        bucket = self.getBucket()
        if toFile and filepath:
            bucket.get_object_to_file(ObjectName, filepath)
            return filepath + " download successfully."
        else:
            object_stream = bucket.get_object(ObjectName)
            if object_stream.client_crc != object_stream.server_crc:
                return object_stream
            else:
                return "download failed."

    def deleteFile(self, ObjectName):
        bucket = self.getBucket()
        if isinstance(ObjectName, str):
            bucket.delete_object(ObjectName)
            return "Successed to delete:\n" + ObjectName
        elif isinstance(ObjectName, list):
            # 每次最多删除1000个文件。
            result = bucket.batch_delete_objects(ObjectName)
            # 打印成功删除的文件名。
            return "Successed to delete:\n" + '\n'.join(result.deleted_keys)

    def checkFileExist(self, ObjectName):
        bucket = self.getBucket()
        exist = bucket.object_exists(ObjectName)
        # 返回值为true表示文件存在，false表示文件不存在。
        if exist:
            return '{} exist'.format(ObjectName)
        else:
            return '{} not eixst'.format(ObjectName)
