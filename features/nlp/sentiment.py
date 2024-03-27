import json
from typing import Tuple

import spacy
import hashlib
import random
import sys
import re
from functools import lru_cache

# import textstat
# import emojis

from transformers import pipeline

class Sentiment():
    """
    Class that implements sentiment analysis in a zero-shot fashion
    """
    def __init__(self, model_name: str = None):
        """
            input
                model_name: str es. 'dbmdz/bert-base-italian-cased'
        """
        self.model_name = model_name

    @lru_cache(maxsize=32)
    def my_pipeline(self, model_name):
        classifier = pipeline("text-classification", model_name)
        return classifier

    def prediction(self, title: str, content: str):
        """
        input:
            @param title: str: string containing the title of a news
            @param content: str: string containing the textual content of a news
        output:
            - dictionary of the prediction in the form {'positive': 1, 'negative': -1, 'overall': 0.5}
        """
        result={
            "description" : "Sentiment Analysis reports the sentiment expressed in the text. A score near to 1 shows a general positive opinion, while a score near to -1 shows a general negative opinion."
        }

        features = {"title" : title, "content" : content}
        classifier=self.my_pipeline(self.model_name)



        for key, value in features.items():
            results = classifier(value)
            print(key, results)
            positivity = 0.0
            negativity = 0.0
            if results[0]['label'] == 'positive':
                positivity = results[0]['score']
            if results[0]['label'] == 'negative':
                negativity = - results[0]['score']
            
            overall = positivity + negativity
                        
            result[key]={
                        "positive":
                        { "description" : f"The score of positive sentiment expressed in the text.",
                            "value": round(positivity,3),
                        },
                        "negative":
                        { "description" : f"The score of negative sentiment expressed in the text.",
                            "value": round(negativity,3),
                        },
                        "overall":                                                
                        { "description" : f"The overall score of sentiment expressed in the text.",
                            "value": round(overall,3),
                        } }

        return result

if __name__ == '__main__':
    # scores = InformalStyle()
    sentiment = Sentiment()

    model_name = 'neuraly/bert-base-italian-cased-sentiment'
    
    title="l'arresto è avvenuto alle 3 del pomeriggio, poverino"
    content='mi piace giocare anche se mi stanca'
    import time

    # Start timer
    start_time = time.perf_counter()

    #for i in range(0,10000):
    print(json.dumps(sentiment.prediction(title, content), indent=4))
    # print(json.dumps(scores.use_of_first_and_second_person(title, content), indent=4))
    exit()
    # print(json.dumps(scores.use_of_interrogative_score(title, content), indent=4))
    # print(json.dumps(scores.use_of_personal_style(title, content), indent=4))
    # print(json.dumps(scores.use_of_modals_score(title, content), indent=4))
    # print(json.dumps(scores.use_of_emoji(title, content), indent=4))
    # print(json.dumps(scores.use_of_interrogative_score(title, content), indent=4))
    # print(json.dumps(scores.use_of_intensifier_score(title, content), indent=4))
    # print(json.dumps(scores.use_of_aggressive_punctuation(title, content), indent=4))
    # print(json.dumps(scores.use_of_shorten_form_score(title, content), indent=4))
    # print(json.dumps(scores.use_of_uncommon_punctuation(title, content), indent=4))
    # print(json.dumps(scores.use_of_uppercase_words(title, content), indent=4))
    # print(json.dumps(scores.use_of_repeated_letters(title, content), indent=4))
    # print(json.dumps(scores.readability_score(title, content), indent=4))
    # End timer
    end_time = time.perf_counter()

    # Calculate elapsed time
    elapsed_time = end_time - start_time
    print("Elapsed time: ", elapsed_time)
    #Elapsed time:  0.15938275000000002
