from flask import Flask, make_response, request, jsonify
import requests
from hide import keys
import Caffe_menu_list
import crawler

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello World!!"


@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    return make_response(jsonify(results()))

def searchLoc(location):
    loc_url = "https://dapi.kakao.com/v2/local/search/address.json?query={}".format(location)
    spec_loc = requests.get(loc_url, headers=headers).json()['documents']
    x = spec_loc[0]['x']
    y = spec_loc[0]['y']
    # (x,y) 좌표
    # print(x,y)
    caffe = []
    url = 'https://dapi.kakao.com/v2/local/search/category.json?category_group_code=CE7&x={}&y={}'.format(x, y)
    places = requests.get(url, headers=headers).json()['documents']
    for place in places[0:10]:
        if place['place_name'].find('토즈') != -1:
            continue
        else:
            caffe.append({'name': place['place_name'], 'url': place['place_url']})
    return caffe

Data = []

Menu = {"menu":['아메리카노','마키아토','카푸치노','라떼','모카','오렌지 주스','레몬에이드','아이스초코','딸기에이드','휘낭시에','스콘','머랭쿠키','마카롱','와플','샌드위치'],
      "price":[4000,4500,4500,4500,5000,5000,6000,5000,6000,2900,2500,2000,2000,5000,4500]
      }

def results():
    req = request.get_json(force=True)
    print(req)
    print('---------------------------------------------')
    event = req.get('queryResult').get('action')
    #print("event: "+event)

    if event=='InputLoc':
        location = req.get('queryResult').get('parameters').get('any')
        info = searchLoc(location)
        print("location: " + location)
        Data.append(info)

        response = \
            {
                'fulfillmentMessages' : [ {
                'text': { 'text':
                        ["1."+info[0]['name']+" 2. "+info[1]['name']+" 3. "+info[2]['name']]
                    }
                }]
            }

    elif event=='selectCaffe':
        selectNum = req.get('queryResult').get('parameters').get('number')-1
        response = \
        {
            'fulfillmentMessages': [{
                'text': {'text':
                             [Data[0][int(selectNum)]['name']+"에서 주문하시겠습니까?"]
                         }
            }]
        }


    return response

Secret = keys.Secret

headers = {
    "Authorization": "KakaoAK " + Secret
}

if __name__ == '__main__':
    app.run(debug=True)
