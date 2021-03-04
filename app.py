from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

import os
import sys
import urllib.request

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta

## HTML을 주는 부분
@app.route('/')
def home():
   return render_template('main.html')

@app.route('/mypage')
def mypage():
   return render_template('mypage.html')

### main page 적용 코드
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

#저장 API
@app.route('/api/save', methods = ['POST'])
def save_trip():
       myRegion_info = request.form['region_give'];
       myPlaceName_info = request.form['placeName_give'];
       myPlaceAddress_info = request.form['placeAddress_give'];
       myPlaceUrl_info = request.form['placeUrl_give'];
       myPlaceNumber_info = request.form['placeNumber_give'];
       myAccommodationName_info = request.form['accommodationName_give'];
       myAccommodationAddress_info = request.form['accommodationAddress_give'];
       myAccommodationUrl_info = request.form['accommodationUrl_give'];
       myAccommodationNumber_info = request.form['accommodationNumber_give'];

       doc = {
          'region': myRegion_info,
          'place_name': myPlaceName_info,
          'place_address': myPlaceAddress_info,
          'place_url': myPlaceUrl_info,
          'place_number' : myPlaceNumber_info,
          'accommodation_name': myAccommodationName_info,
          'accommodation_address': myAccommodationAddress_info,
          'accommodation_url': myAccommodationUrl_info,
          'accommodation_number': myAccommodationNumber_info
       }
       db.myTrip.insert_one(doc)
       return jsonify({'msg': '저장완료!'})

## my page 적용 코드
# my page review 저장 함수
@app.route('/api/review', methods=['POST'])
def save_review():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload["id"]})
        review_receive = request.form["review_give"]
        date_receive = request.form["date_give"]
        doc = {
            "username": user_info["username"],
            "review": review_receive,
            "date": date_receive
        }
        db.reviews.insert_one(doc)
        return jsonify({"result": "success", 'msg': '포스팅 성공'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))



# my page 여행 삭제 함수
@app.route('/api/delete', methods=['POST'])
def delete_travel():
   db.users.delete_one({'name':'bobby'})
   return jsonify({'result':'success', 'msg': location_receive})

@app.route('/api/getMyPage', methods = ['GET'])
def listing():
   review_data = list(db.myTrip.find({}, {'_id':False}))
   return jsonify({'all_reviewdata': review_data})

if __name__ == '__main__':  
   app.run('0.0.0.0',port=5000,debug=True)

   