from flask import Flask,make_response,request,jsonify
import requests
from hide import keys


app = Flask(__name__)

@app.route('/')
def index():
    return "Hello World!!"

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    return make_response(jsonify(results()))

def results():
    req = request.get_json(force=True)
    print(req)
    print('---------------------------------------------')
    queryText = req.get('queryResult').get('queryText')
    queryDateTime = req.get('queryResult').get('parameters').get('date-time')
    queryNumber = req.get('queryResult').get('parameters').get('number-integer')
    location = req.get('queryResult').get('parameters').get('any')
    print("date-time: "+queryDateTime)
    print("number-integer: " + str(queryNumber))
    print("queryText: "+queryText)
    print("location: "+location)
    searchLoc(location)
    response = \
    {
        'fulfillmentMessages': [ {
            'text' : { 'text':
                [searchLoc(location)[0]]
            }
        }]
    }
    return response

Secret = keys.Secret

headers = {
    "Authorization": "KakaoAK "+Secret
}

def searchLoc(location):
    loc_url = "https://dapi.kakao.com/v2/local/search/address.json?query={}".format(location)
    spec_loc = requests.get(loc_url, headers = headers).json()['documents']
    x = spec_loc[0]['x']
    y = spec_loc[0]['y']
    #(x,y) 좌표
    #print(x,y)
    caffe = []
    url = 'https://dapi.kakao.com/v2/local/search/category.json?category_group_code=CE7&x={}&y={}'.format(x, y)
    places = requests.get(url, headers=headers).json()['documents']
    for place in places[0:10]:
        if place['place_name'].find('토즈')!=-1:
            continue
        else:
            caffe.append(place['place_name'])
            #print(place['place_name'] + ': ' + place['place_url'])
    return caffe[0:3]

if __name__ == '__main__':
    app.run(debug=True)