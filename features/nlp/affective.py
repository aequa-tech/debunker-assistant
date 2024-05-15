import json
from functools import lru_cache
from transformers import pipeline

from features.nlp.affective_language.affective_en import Sentiment_en, Emotion_en
from features.nlp.affective_language.affective_it import Sentiment_it, Emotion_it


class Sentiment():
    """
    Class that implements sentiment analysis in a zero-shot fashion
    """
    def __init__(self):
        self.sentiment_it=Sentiment_it()
        self.sentiment_en=Sentiment_en()



    def get_sentiment_positive(self, language, title: str, content: str):

        if language == 'it':
            return self.sentiment_it.get_sentiment_positive(title, content)
        elif language == 'en':
            return self.sentiment_en.get_sentiment_positive(title, content)
        else:
            return None

    def get_sentiment_negative(self, language, title: str, content: str):

        if language == 'it':
            return self.sentiment_it.get_sentiment_negative(title, content)
        elif language == 'en':
            return self.sentiment_en.get_sentiment_negative(title, content)
        else:
            return None

class Emotion():
    """
    Class that implements sentiment analysis in a zero-shot fashion
    """
    def __init__(self):
        self.emotion_it=Emotion_it()
        self.emotion_en=Emotion_en()


    def get_emotion_joy(self, language, title: str, content: str):

        if language == 'it':
            return self.emotion_it.get_emotion_joy(title, content)
        elif language == 'en':
            return self.emotion_en.get_emotion_joy(title, content)
        else:
            return None


    def get_emotion_sadness(self, language, title: str, content: str):

        if language == 'it':
            return self.emotion_it.get_emotion_sadness(title, content)
        elif language == 'en':
            return self.emotion_en.get_emotion_sadness(title, content)
        else:
            return None



    def get_emotion_fear(self, language, title: str, content: str):

        if language == 'it':
            return self.emotion_it.get_emotion_fear(title, content)
        elif language == 'en':
            return self.emotion_en.get_emotion_fear(title, content)
        else:
            return None

    def get_emotion_anger(self, language, title: str, content: str):

        if language == 'it':
            return self.emotion_it.get_emotion_anger(title, content)
        elif language == 'en':
            return self.emotion_en.get_emotion_anger(title, content)
        else:
            return None



if __name__ == '__main__':

    sentiment = Sentiment()
    emotion = Emotion()
    apis ={
        "affectiveStyle": {
            'joy': emotion.get_emotion_joy,
            'sadness': emotion.get_emotion_sadness,
            'fear': emotion.get_emotion_fear,
            'anger': emotion.get_emotion_anger,
            'positiveSentiment': sentiment.get_sentiment_positive,
            'negativeSentiment': sentiment.get_sentiment_negative,
        },


    }

    for key, value in apis.items():
        for key2, value2 in value.items():
            print(key,key2)
            print(value2("it","titolo di prova","contenuto di prova")["title"]["descriptions"]["absolute"])
            print(value2("en","titolo di prova","contenuto di prova")["title"]["descriptions"]["absolute"])

