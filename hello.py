from flask import Flask,make_response,request,jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello World!!"

@app.route('/webhook', methods=['GET','POST'])
def webhook():
    return make_response(jsonify(results()))

def results():
    req = request.get_json(force=True)
    print('input:'+req)
    print('-------------------------------')
    queryText = req.get('queryResult').get('queryText')
    print(queryText)

    response =\
        {
            'fulfillmentMessages':[{
                'text':{'text':
                        ["this is a response from webhook."]
                    }
            }]
        }
    return response

if __name__ == '__main__':
    app.run(debug=True)