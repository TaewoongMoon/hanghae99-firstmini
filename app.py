import urllib.request
import sys
import os
from flask import Flask, render_template, jsonify, request
app = Flask(__name__)


# HTML을 주는 부분

@app.route('/')
def home():
    return render_template('main.html')


# API 역할을 하는 부분
@app.route('/review', methods=['POST'])
def test_post1():

    client_id = "6b0ouK3enTeVd0V27qWi"
    client_secret = "ih_5zXNVN2"

    encText = urllib.parse.quote("title_give")

    url = "https://openapi.naver.com/v1/search/blog?query=" + encText  # json 결과
    # url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # xml 결과

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()

    if(rescode == 200):
        response_body = response.read()
        print(response_body.decode('utf-8'))
    else:
        print("Error Code:" + rescode)

    return jsonify({'result': 'success', 'msg': response})

    @app.route('/delete', methods=['POST'])
    def test_post2():
        title_receive = request.form['title_give']
        print(title_receive)

        return jsonify({'result': 'success', 'msg': '이 요청은 POST!'})

        if __name__ == '__main__':
            app.run('0.0.0.0', port=5000, debug=True)
