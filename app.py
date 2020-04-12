import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restful import Api, Resource
import json
import altair as alt
import numpy as np
import pandas as pd
from datetime import datetime
from collections import OrderedDict

app = Flask(__name__)
CORS(app)
api = Api(app)

if not os.path.isfile('dev.speakai.api.json'):
    exit('No analytics data available !')

with open('dev.speakai.api.json') as f:
    data = json.load(f)

# Learns the earliest and nearest dates for processed analytics
def figure_out_daterange(analytics):
    earliestDate = datetime.now()
    presentDate = datetime.now()
    for upload in analytics:
        if (np.datetime64(upload['createdAt'], 'D') < np.datetime64(earliestDate, 'D')):
            earliestDate = upload['createdAt']
            # print(upload['createdAt'], ' is earlier than ', earliestDate)

    return np.arange(np.datetime64(earliestDate), np.datetime64(presentDate), dtype='datetime64[D]')

def compute_activity_data(analytics, daterange):
    dictionary = {}  # to hold to activity (value) by date (key)
    # put initial zero activity on each date
    for date in daterange:
        dictionary[date] = {
            'totalTime': 0,
            'totalBytes': 0,
            'totalCount': 0,
            'sources': [],
        }

    print('Loop through analytics and count total duration...')
    for upload in analytics:
        ref = dictionary[np.datetime64(upload['createdAt'], 'D')]
        ref['totalTime'] += int(float(upload['duration']['inSecond']))
        ref['totalCount'] += 1
        key = np.datetime64(upload['createdAt'], 'D')
        dictionary[key] = ref
        #dictionary[datetime(upload.createdAt).date]

    return dictionary

def compute_activity(activityData, by='totalTime'):
    activity = []
    for upload in activityData:
        activity.append(activityData[upload].get(by))
    return activity

class Generator(Resource):
    @staticmethod
    def get():
        # Obtain analytics data
        analyticsData = data[0]

        # Generate Graph Specs
        ## figure out date range
        x = figure_out_daterange(analyticsData)

        ## compute activity data
        activityData = compute_activity_data(analyticsData, x)

        ## compute activity
        f_of_x = compute_activity(activityData, 'totalTime')

        ## generate graph specs
        graph_data = pd.DataFrame({
            'x': x,
            'f(x)': f_of_x,
        })
        graph_spec = alt.Chart(graph_data).mark_line().encode(
            x = 'x',
            y = 'f(x)'
        )

        return graph_spec.to_json()


api.add_resource(Generator, '/')

