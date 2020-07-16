from flask import Flask

app = Flask(__name__)

@app.route('/json/object')
def get_json_object():
    response = {"id":1}
    return response
if __name__ == '__main__':
    app.run(debug=True)