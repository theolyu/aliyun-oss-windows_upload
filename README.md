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
