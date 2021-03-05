from flask import Flask, render_template, jsonify, request, redirect, url_for

import os
import sys
import urllib.request

from pymongo import MongoClient
import jwt
import datetime
import hashlib
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta

from bson.objectid import ObjectId


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

SECRET_KEY = 'SPARTA'
client = MongoClient('localhost', 27017)
db = client.tat.users

## HTML을 주는 부분

@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload["id"]})
        return render_template('index.html', user_info=user_info)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))

@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html')

@app.route('/mypage')
def mypage():
    msg = request.args.get("msg")
    return render_template('mypage.html')

# 로그인 페이지를 위한 함수
@app.route('/sign_in', methods=['POST'])
def sign_in():
   # 로그인
   username_receive = request.form['username_give']
   password_receive = request.form['password_give']
   pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
   result = db.users.find_one({'username': username_receive, 'password': pw_hash})

   if result is not None:
      payload = {
      'id': username_receive,
      'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
      }
      token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

      return jsonify({'result': 'success', 'token': token})
   # 찾지 못하면
   else:
      return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"username": username_receive}))
    print(exists)
    return jsonify({'result': 'success', 'exists': exists})

@app.route('/sign_up/save', methods=['POST'])
def sign_up():
   username_receive = request.form['username_give']
   password_receive = request.form['password_give']
   password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
   doc = {
      "username": username_receive,                               # 아이디
      "password": password_hash,                                  # 비밀번호
      "profile_name": username_receive,                           # 프로필 이름 기본값은 아이디
      "profile_pic": "",                                          # 프로필 사진 파일 이름
      "profile_pic_real": "profile_pics/profile_placeholder.png", # 프로필 사진 기본 이미지
      "profile_info": ""                                          # 프로필 한 마디
   }
   db.users.insert_one(doc)
   return jsonify({'result': 'success'})

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
   client_id = "nMm0qI07MHER7JFknCGp"
   client_secret = "BcBS7jNooM"
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

#저장 API
@app.route('/api/save', methods = ['POST'])
def save_trip():
      token_receive = request.cookies.get('mytoken')
      try:
         payload = jwt.decode(token_receive, SECRET_KEY, algorithms = ['HS256'])
         myRegion_info = request.form['region_give'];
         myPlaceName_info = request.form['placeName_give'];
         myPlaceAddress_info = request.form['placeAddress_give'];
         myPlaceUrl_info = request.form['placeUrl_give'];
         myPlaceImg_info = request.form['placeImg_give'];
         myAccommodationName_info = request.form['accommodationName_give'];
         myAccommodationAddress_info = request.form['accommodationAddress_give'];
         myAccommodationUrl_info = request.form['accommodationUrl_give'];
         username = payload['id']
         doc = {
         'username': username,
         'region': myRegion_info,
         'place_name': myPlaceName_info,
         'place_address': myPlaceAddress_info,
         'place_url': myPlaceUrl_info,
         'place_img': myPlaceImg_info,
         'accommodation_name': myAccommodationName_info,
         'accommodation_address': myAccommodationAddress_info,
         'accommodation_url': myAccommodationUrl_info,
         }
         print(doc)
         db.myTrip.insert_one(doc)
         return jsonify({'msg': '저장완료!'})
      except(jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
         return redirect(url_for('home'))

## my page 적용 코드

# my page 여행 삭제 함수
@app.route('/api/delete', methods=['POST'])
def delete_travel():
   token_receive = request.cookies.get('mytoken')
   try:
      payload = jwt.decode(token_receive, SECRET_KEY, algorithms = ['HS256'])
      user_info = list(db.myTrip.find({'username': payload['id']}))
      trip_id_receive = request.form["trip_id_give"]
      db.myTrip.delete_one({'_id':ObjectId(trip_id_receive)})
      return jsonify({'result':'success', 'msg': '삭제 완료!'})
   except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
      return redirect(url_for('home'))

# review 저장 함수
@app.route('/api/review', methods=['POST'])
def review_travel():
   token_receive = request.cookies.get('mytoken')
   try:
      payload = jwt.decode(token_receive, SECRET_KEY, algorithms = ['HS256'])
      user_info = list(db.myTrip.find({'username': payload['id']}))
      trip_id_receive = request.form["trip_id_give"]
      review_receive = request.form["review_give"]
      print(review_receive)
      test = db.myTrip.update_one({'_id':ObjectId(trip_id_receive)},{'$set':{'review':review_receive}},upsert=True)
      return jsonify({'result':'success', 'msg': '리뷰 저장 완료!'})
   except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
      return redirect(url_for('home'))

#mypage에 데이터 내리는 API
@app.route('/api/getMyPage', methods = ['GET'])
def mypage_listing():
   token_receive = request.cookies.get('mytoken')
   try:
      payload = jwt.decode(token_receive, SECRET_KEY, algorithms = ['HS256'])
      user_info = list(db.myTrip.find({'username': payload['id']}))
      for data in user_info:
         data['_id'] = str(data['_id'])
      return jsonify({'mypage_data': user_info})
   except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
      return redirect(url_for('home'))


if __name__ == '__main__':  
   app.run('0.0.0.0',port=5000,debug=True)

   