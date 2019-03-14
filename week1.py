from flask import Flask, make_response
from flask import request

app = Flask(__name__)


@app.route('/')
def hello_world():
    print(request.headers)
    return 'Index!'


@app.route('/custom_header')
def custom_header():
    my_resp = make_response('Response')
    my_resp.headers['custom_header'] = '<script> alert("Hi!")</script>'
    return my_resp


if __name__ == "__main__":
    app.run(debug=True, port=8080)
