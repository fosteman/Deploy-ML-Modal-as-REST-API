import os
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import json
import altair as alt
import numpy as np
import pandas as pd
from datetime import datetime

app = Flask(__name__)
api = Api(app)

if not os.path.isfile('dev.speakai.api.json'):
    exit('No analytics data available !')

with open('dev.speakai.api.json') as f:
    data = json.load(f)

# Learns the earliest and nearest dates for processed analytics
def figure_out_daterange(analytics):
    earliestDate = datetime.now()
    presentDate = datetime.now()
    for upload in analytics[0]:
        if (np.datetime64(upload['createdAt'], 'D') < np.datetime64(earliestDate, 'D')):
            earliestDate = upload['createdAt']
            # print(upload['createdAt'], ' is earlier than ', earliestDate)

    return np.arange(np.datetime64(earliestDate), np.datetime64(presentDate), dtype='datetime64[D]')

class Generator(Resource):
    @staticmethod
    def get():
        # Obtain analytics data
        analyticsData = data[0:9]

        # Generate Graph Specs
        ## figure out date range
        figure_out_daterange(analyticsData)

        return jsonify({
            'data': analyticsData[0],
            'specs': 'Vega Graph Specs! '
        })


api.add_resource(Generator, '/graph')

if __name__ == '__main__':
    app.run(debug=True)


