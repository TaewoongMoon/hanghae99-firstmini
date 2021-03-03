from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

import os
import sys
import urllib.request

## HTML을 주는 부분
@app.route('/')
def home():
   return render_template('main.html')

### main page 내 함수
@app.route('/api/search-1', methods=['POST']) # 해당 주소와 형식으로 API 요청이 오면 아래 함수를 실행
def search_place(): 
   # 'location_give(클라이언트 data의 key 값)'의 value를 받아 " 명소"를 합친다.
   search_word = request.form['region_give'] + " 명소"
   # 위 변수를 가지고 네이버 검색 요청 함수를 실행하여 반환 값을 저장
   result_return = search(search_word)
   return jsonify({"places" : result_return}) # 함수의 리턴 값을 json 형태로 클라이언트에 반환

@app.route('/api/search-2', methods=['POST'])
def search_accommodation(): 
   search_word = request.form['place_give'] + " 숙소"
   result_return = search(search_word)
   return jsonify({"accommodations" : result_return})

# 네이버 검색 요청 함수
def search(value):
   client_id = ""
   client_secret = ""
   encText = urllib.parse.quote(value) # 지역변수 value 값을 넣어 url 에 넣을 값으로 변경해줌
   url = "https://openapi.naver.com/v1/search/local.json?query=" + encText +  "&display=5" + "&sort=comment" # json 결과
   # url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # xml 결과
   request = urllib.request.Request(url)
   request.add_header("X-Naver-Client-Id",client_id)
   request.add_header("X-Naver-Client-Secret",client_secret)
   response = urllib.request.urlopen(request)
   rescode = response.getcode()
   if(rescode==200):
      response_body = response.read()
      result = response_body.decode('utf-8') # 출력해보니 json 형태의 값
      return result # json 형태의 결과값을 반환
   else:
      print("Error Code:" + rescode)


# myPage review 저장 함수
@app.route('/api/review', methods=['POST'])
def save_review():
   location_receive = request.form['data_give']
   search_attraction(location_receive)
   return jsonify({'result':'success', 'msg': location_receive})

# myPage 여행 삭제 함수
@app.route('/api/delete', methods=['POST'])
def delete_travel():
   location_receive = request.form['data_give']
   search_attraction(location_receive)
   return jsonify({'result':'success', 'msg': location_receive})

if __name__ == '__main__':  
   app.run('0.0.0.0',port=5000,debug=True)

   