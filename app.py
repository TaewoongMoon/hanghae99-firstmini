from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

import os
import sys
import urllib.request

## HTML을 주는 부분
@app.route('/')
def home():
   return render_template('mypage.html')

location_receive = "서울 명소"

# API 역할을 하는 부분
@app.route('/review', methods=['GET'])
def test_post1():
   client_id = "-"
   client_secret = "-"
   encText = urllib.parse.quote(location_receive)
   url = "https://openapi.naver.com/v1/search/local.json?query=" + encText + "&display=5" + "&sort=comment" # json 결과
   # url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # xml 결과
   request = urllib.request.Request(url)
   request.add_header("X-Naver-Client-Id",client_id)
   request.add_header("X-Naver-Client-Secret",client_secret)
   response = urllib.request.urlopen(request)
   rescode = response.getcode()
   if(rescode==200):
      response_body = response.read()
      print(response_body.decode('utf-8'))
   else:
      print("Error Code:" + rescode)
   return jsonify({'result':'success', 'msg': "성공!!"})

@app.route('/delete', methods=['POST'])
def test_post2():
   location_receive = request.form['location_give']
   return jsonify({'result':'success', 'msg': location_receive})

if __name__ == '__main__':  
   app.run('0.0.0.0',port=5000,debug=True)

   