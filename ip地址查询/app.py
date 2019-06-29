# coding=utf-8

from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ip/', methods=['GET', 'POST'])
def ip_():
    if request.method == 'GET':
        return render_template('ip_query.html')
    else:
        ip_addr = request.form.get('ip')
        url = "http://apis.juhe.cn/ip/ipNew?ip=%s&key=286b55f6bbf4f525cf1a73707609f866" % ip_addr
        response = requests.get(url)
        data = json.loads(response.text)
        if data['resultcode'] == '200':
            item = data['result']
            return render_template('ip_query_result.html', item=item)
        else:
            return data['reason']


@app.route('/history_today/', methods=['POST', 'GET'])
def history_today():
    if request.method == 'GET':
        return render_template('history_today_query.html')
    else:
        m_and_d = request.form.get('m_and_d')
        try:
            month = m_and_d.strip().split(' ')[0]
            day = m_and_d.strip().split(' ')[1]
        except:
            return '月份或者天数没写'
        url = "http://api.juheapi.com/japi/toh?key=5d51acbca0959473936239c7f8ecc5ae&v=1.0&month=%s&day=%s" % (month, day)
        response = requests.get(url)
        data = json.loads(response.text)
        if data['reason'] == '错误的请求参数':
            return data['reason']
        else:
            items = data['result']
            return render_template('history_today.html', items=items)

if __name__ == '__main__':
    app.run()
