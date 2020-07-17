from flask import Flask,make_response,request,jsonify

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
    location = req.get('queryResult').get('queryText')
    color = req.get('queryResult').get('outputContexts')[0].get('parameters').get('color')
    size = req.get('queryResult').get('outputContexts')[0].get('parameters').get('size')
    print(color)
    print(size)
    print(location)

    response = \
    {
        'fulfillmentMessages': [ {
            'text' : { 'text':
                [location+"로 "+color+'색상'+size+'를 보내드릴게요!' ]
            }
        }]
    }
    return response

if __name__ == '__main__':
    app.run(debug=True)