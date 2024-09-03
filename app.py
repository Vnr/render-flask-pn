from flask import Flask, Response, request, jsonify
import logging
import requests
import base64
import re

app = Flask(__name__)
#flask --app main run

proxies = {
       u'http': 'http://127.0.0.1:8888',
       u'https': 'http://127.0.0.1:8888'
}
#s.proxies = proxies
#s.verify = False
requests.packages.urllib3.disable_warnings()

@app.route('/', methods=["GET"])
def hello_world():
    return "Hello World"


@app.route('/requeststest')
def requeststest():
#http://127.0.0.1:5000/requeststest
    import requests
    return requests.get("https://httpbin.org/get",
                        #proxies=proxies,
                        verify = False,
    					headers={'Referer': 'https://pamyat-naroda.ru/', 'User-Agent': 'Mozilla New'}).content  # verify=False not working


@app.route('/gettoken')
def get_token():
    r = requests.get(u'https://pamyat-naroda.ru/',
                     #proxies=proxies,
                     verify = False,
                     headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko'}) #, proxies=proxies, verify=False)
    #print(u'Got new cookies')
    #token = r.cookies.get_dict()['ssobda88568a54f922fcdfc6dbf940e5d00']
    m = re.search('data-st-hash="([^"]+)"', r.text)
    token = m.group(1)
    token += "="
    token = token.replace('-', '+').replace('_', '/')
    token = base64.b64decode(token).decode("utf-8")
    return token.replace('XXXXXX', '/').split('YYYYYY')[0]


@app.route('/obd/<path:path>', methods=['GET','POST'])
def proxy(path):
    
    #return request.method + "<br>" + request.url_root + "<br>" + request.data
    # http://flask.pocoo.org/docs/0.10/api/#flask.Request.get_json
    # request.get_data()    # To get the raw data, regardless of content type.
    # page = request.args.get("page")
    # password = request.form.get('password')
    
    url = 'https://cdn.pamyat-naroda.ru/data/' + get_token() + '/' + path

    
    #https://cloud.google.com/appengine/docs/standard/python/issue-requests
    result = requests.post(url=url,
        data=request.data,
        verify = False,
        #proxies=proxies,
        headers={'Referer': 'https://pamyat-naroda.ru/', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko'})

#    if result.status_code == 200:
#      doSomethingWithResult(result.content)
    return Response(result.content, headers={'Access-Control-Allow-Origin': '*', 'URL':url})
