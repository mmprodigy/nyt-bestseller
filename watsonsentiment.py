import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
import watson_developer_cloud.natural_language_understanding.features.v1 \
  as Features

#import the dicitionary with all rest of the features 

natural_language_understanding = NaturalLanguageUnderstandingV1(
  username="username", 
  password="password",
  version="2017-02-27")

response = natural_language_understanding.analyze(
  text="IBM is an American multinational technology company headquartered \
    in Armonk, New York, United States, with operations in over 170 \
    countries.", #book review inserted here or description
  features=[
    Features.Emotion(
      # Emotion options
      targets=["apples","oranges"] #whatever is important ... also generates document wide ones
    )
    Features.Semtiment(
      targets=[
       "book","novel", "story", "plot"
      ]
    ),
    Features.Keywords(
      emotion=True,
      sentiment=True,
      limit=5
    )
  ]
)

print(json.dumps(response, indent=2))




'''{
  "usage": {
    "text_units": 1,
    "text_characters": 140,
    "features": 2
  },
  "language": "en",
  "keywords": [
    {
      "text": "American multinational technology",
      "sentiment": {
        "score": 0.0
      },
      "relevance": 0.993518,
      "emotion": {
        "sadness": 0.085259,
        "joy": 0.026169,
        "fear": 0.02454,
        "disgust": 0.088711,
        "anger": 0.033078
      }
    },
    {
      "text": "New York",
      "sentiment": {
        "score": 0.0
      },
      "relevance": 0.613816,
      "emotion": {
        "sadness": 0.166741,
        "joy": 0.228903,
        "fear": 0.057987,
        "disgust": 0.050965,
        "anger": 0.054653
      }
    }
  ],
 }'''

#This is the output 


 '''document": {
      "score": 0.127034,
      "label": "positive"
    }''' #also returns document sentiment