import json

from flask import Flask, request, jsonify, Response
from gevent import pywsgi
from gevent import monkey

from aliyunOSSRun import RunOSS

monkey.patch_all()
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
    # app.run(debug=False, port=5001, host='0.0.0.0')   # 启动服务。默认端口号是5000

    port = 5001  # 默认端口号是5000
    server = pywsgi.WSGIServer(('0.0.0.0', port), app)
    server.serve_forever()
