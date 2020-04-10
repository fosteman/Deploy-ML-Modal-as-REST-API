import os
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import json

app = Flask(__name__)
api = Api(app)

if not os.path.isfile('dev.speakai.api.json'):
    exit('No analytics data available !')

with open('dev.speakai.api.json') as f:
  data = json.load(f)

class Generator(Resource):
    @staticmethod
    def get():

        graphSpec = data
        return jsonify({
            'specs': graphSpec
        })


api.add_resource(Generator, '/graph')

if __name__ == '__main__':
    app.run(debug=True)
