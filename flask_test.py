from flask import Flask
from flask import request
from urllib.parse import unquote
#创建Flask的实例对象
app = Flask(__name__)

#装饰器
@app.route('/')
def hello_world():
    #视图函数
    return 'Hello World!'
@app.route('/sendSms')
def send_msg():
    api_key = request.headers.get('apiKey')
    template_id = request.headers.get('templateId')
    singature_id = request.headers.get('singatureId')
    phones = request.headers.get('phones')
    content = request.headers.get('content')
    print(request.args.get('content'))
    headers = {
        "apikey":api_key,
        "templateId": template_id,
        "singatureId": singature_id,
        "phones":phones
    }
    print("headers:")
    print(headers)
    print("-----------------")
    print("content:")
    print(unquote(content))
    return content
@app.route('/influxdb/v1/write',methods=['POST'])
def write():
    print(request.get_data())
    return {'code':0}
if __name__ == '__main__':
    # app.config['JSON_AS_ASCII'] = False
    app.run(host='0.0.0.0',port=9090,debug=True)