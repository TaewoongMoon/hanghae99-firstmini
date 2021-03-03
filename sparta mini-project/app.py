from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

import os
import sys
import urllib.request
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta
## HTML을 주는 부분
@app.route('/')
def home():
   return render_template('main.html')

### API 역할을 하는 부분

# myPage review 저장 함수
@app.route('/api/review', methods=['POST'])
def save_review():
   location_receive = request.form['data_give']
   search(location_receive)
   return jsonify({'result':'success', 'msg': location_receive})

# myPage 여행 삭제 함수
@app.route('/api/delete', methods=['POST'])
def delete_travel():
   location_receive = request.form['data_give']
   search(location_receive)
   return jsonify({'result':'success', 'msg': location_receive})


# 명소 검색 API
@app.route('/api/search-1', methods=['POST'])
def test_post2():
   region_receive = request.form['region_give'] + "명소"
   result_return = search(region_receive)
   return jsonify({'places' : result_return})
 
def search(value):
   client_id = "fF9Iz38iGVyIuiNb8mZZ"
   client_secret = "JLVNkEsRDb"
   encText = urllib.parse.quote(value)
   url = "https://openapi.naver.com/v1/search/local.json?query=" + encText +  "&display=5" + "&sort=comment" # json 결과
   # url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # xml 결과
   request = urllib.request.Request(url)
   request.add_header("X-Naver-Client-Id", client_id)
   request.add_header("X-Naver-Client-Secret", client_secret)
   response = urllib.request.urlopen(request)
   rescode = response.getcode()
   if(rescode==200):
      response_body = response.read()
      result = response_body.decode('utf-8')
      print(result)
      return result
   else:
      print("Errosr Code:" + rescode)

# 숙소 검색 API
@app.route('/api/search-2', methods=['POST'])
def test_post3():
   place_receive = request.form['place_give'] + "숙박"
   result_return2 = search(place_receive)
   return jsonify({'accommodations' : result_return2})
 


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

#DB에 저장된 데이터들 불러오기
@app.route('/api/getMyPage', methods = ['GET'])
def listing():
   review_data = list(db.myTrip.find({}, {'_id':False}))
   print(review_data)
   return jsonify({'all_reviewdata': review_data})

if __name__ == '__main__':  
   app.run('0.0.0.0',port=5000,debug=True)