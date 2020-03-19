from flask import Flask
from predict import Predictor
from flask import request, jsonify
import json
from flask_cors import CORS


app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/previsao', methods=['POST'])
def predict():
	return Predictor().main(request.json)


@app.route('/', methods=['GET'])
def home():

   return  app.response_class(response=json.dumps("API is running"),
                                status=200,
                                mimetype='application/json')

if __name__ == '__main__':
	app.run(port=5000)
