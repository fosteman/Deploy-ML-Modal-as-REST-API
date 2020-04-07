# Ref: https://towardsdatascience.com/deploy-your-machine-learning-model-as-a-rest-api-4fe96bf8ddcc

import os
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import nltk
nltk.download('punkt')
# from model.Train import train_model
from sklearn.externals import joblib

app = Flask(__name__)
api = Api(app)

# if not os.path.isfile('text-model.model'):
#     train_model()

# model = joblib.load('text-model.model')

class MakePrediction(Resource):
    @staticmethod
    def post():
        posted_data = request.get_json()
        text = posted_data['text']
        sentences = nltk.tokenize.sent_tokenize(text)
        print(sentences)

        #install textblob if not already installed using "pip install -U textblob"
        from textblob import TextBlob

        print('{:40} : {:10} : {:10}'.format("Review", "Polarity", "Subjectivity") )
        
        resultList = []
        #Categorize Polarity into Positive, Neutral or Negative
        labels = ["Negative", "Neutral", "Positive"]
        #Initialize count array
        values =[0,0,0]
        
        for review in sentences:
            #Find sentiment of a review
            sentiment = TextBlob(review)
            #Print individual sentiments
            x = {
                "sentence": review, 
                "polarity": sentiment.polarity, 
                "subjectivity": sentiment.subjectivity
            }
            resultList.append(x)
            polarity = round(( sentiment.polarity + 1 ) * 3 ) % 3
    
            #add the summary array
            values[polarity] = values[polarity] + 1

            print('{:40} :   {: 01.2f}    :   {:01.2f}'.format(review[:40]\
                        , sentiment.polarity, sentiment.subjectivity) )

        analysis = {
            "Negative": values[0],
            "Neutral": values[1],
            "Positive": values[2]
        }
        print("Final summarized counts :", analysis)

        return jsonify({
            'analysis': analysis,
            'Prediction': resultList
        })

api.add_resource(MakePrediction, '/predict')

if __name__ == '__main__':
    app.run(debug=True)
