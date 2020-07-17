import requests
from hide import keys

import crawler

Secret = keys.Secret

headers = {
    "Authorization": "KakaoAK "+Secret
}

def searchLoc(location):
    loc_url = "https://dapi.kakao.com/v2/local/search/address.json?query={}".format(location)
    spec_loc = requests.get(loc_url, headers = headers).json()['documents']
    x = spec_loc[0]['x']
    y = spec_loc[0]['y']
    print(x,y)
    url = 'https://dapi.kakao.com/v2/local/search/category.json?category_group_code=CE7&x={}&y={}'.format(x, y)
    places = requests.get(url, headers=headers).json()['documents']
    for place in places:
        print(place['place_name'] + ': ' + place['place_url'])
searchLoc('역삼동')

