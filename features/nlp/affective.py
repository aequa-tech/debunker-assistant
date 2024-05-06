import json
from functools import lru_cache
from transformers import pipeline

class Sentiment():
    """
    Class that implements sentiment analysis in a zero-shot fashion
    """
    def __init__(self):
        self.model_name={}
        self.classifier={}
        self.model_name["it"] = 'neuraly/bert-base-italian-cased-sentiment'
        self.model_name["en"] = 'neuraly/bert-base-italian-cased-sentiment'

    @lru_cache(maxsize=32)
    def __my_pipeline(self, model_name):
        classifier = pipeline("text-classification", model_name)
        return classifier

    @lru_cache(maxsize=32)
    def __prediction(self, language: str, title: str, content: str):
        """
        input:
            @param title: str: string containing the title of a news
            @param content: str: string containing the textual content of a news
        output:
            - dictionary of the prediction in the form {'positive': 1, 'negative': -1, 'overall': 0.5}
        """
        result={
            'positive' : {

                'description': {
                                'en': 'The score of positive sentiment expressed in the text.',
                                'it': 'descrizione in italiano'
                               }

            },
            'negative' :{
                'description': {
                                'en': 'The score of negative sentiment expressed in the text.',
                                'it': 'descrizione in italiano'
                               }

             }
        }

        features = {"title" : title, "content" : content}
        #classifier= pipeline("text-classification", self.model_name)
        #classifier=self.__my_pipeline(self.model_name)

        for key, value in features.items():
            print(value)
            classifier=self.__my_pipeline(self.model_name[language])
            results = classifier(value,truncation=True)
            #results = classifier(value)
            # print(key, results)
            positivity = 0.0
            negativity = 0.0
            negativity_absolute = 0
            positivity_absolute = 0
            if results[0]['label'] == 'positive':
                positivity = results[0]['score']
                positivity_absolute = 1 if results[0]['score'] >= 0.5 else 0 
            if results[0]['label'] == 'negative':
                negativity = - results[0]['score']
                negativity_absolute = 1 if results[0]['score'] >= 0.5 else 0
            
            # overall = positivity + negativity
            
            result['positive'][key]={
                           "values" : {

                               "absolute": positivity_absolute,
                               "local_normalisation": round(positivity, 3),
                               "global_normalisation": None,
                           },

                          'descriptions': {
                              'absolute': {'en': '', 'it': ''},
                              'local_normalisation': {'en': '', 'it': ''},
                              'global_normalisation': {'en': None, 'it': None}
                          }
            }

            result['negative'][key]={
                           "values" : {

                               "absolute": negativity_absolute,
                               "local_normalisation": round(negativity, 3),
                               "global_normalisation": None,
                           },

                          'descriptions': {
                              'absolute': {'en': '', 'it': ''},
                              'local_normalisation': {'en': '', 'it': ''},
                              'global_normalisation': {'en': None, 'it': None}
                          }
            }


        return result



    def __get_sentiment(self, language, title: str, content: str, phenomena):
        prediction = self.__prediction(language,title, content)
        result = prediction[phenomena]


        return result


    def get_sentiment_positive(self,language,title, content):

        return self.__get_sentiment(language,title, content, phenomena="positive")

    def get_sentiment_negative(self,language,title, content):

        return self.__get_sentiment(language,title, content, phenomena="negative")

class Emotion():
    """
    Class that implements sentiment analysis in a zero-shot fashion
    """
    def __init__(self):
        self.model_name ={}
        self.model_name["it"] = "MilaNLProc/feel-it-italian-emotion"
        self.model_name["en"] = "MilaNLProc/feel-it-italian-emotion"
        #self.classifier = pipeline("text-classification", self.model_name)

    @lru_cache(maxsize=32)
    def my_pipeline(self, model_name):
        classifier = pipeline("text-classification", model_name)
        return classifier

    @lru_cache(maxsize=32)
    def __prediction(self, language, title: str, content: str):
        """
        input:
            @param title: str: string containing the title of a news
            @param content: str: string containing the textual content of a news
        output:
            - dictionary of the prediction of each emotion
        """
        result={

            "joy" : {
                "description" : {
                "en" : "The score of presence of joy expressed in the text.",
                "it" : ""
              }
            },
            "sadness" :  {
                "description" : {
                "en" : "The score of presence of sadness expressed in the text.",
                "it" : ""
              }
            },
            "fear" :  {
                "description" : {
                "en" :  "The score of presence of fear expressed in the text.",
                "it" : ""
              }
            },
            "anger" :  {
                "description" : {
                "en" : "The score of presence of anger expressed in the text.",
                "it" : ""
              }
            },

        }

        features = {"title" : title, "content" : content}
        #classifier=self.my_pipeline(self.model_name)
        #classifier = pipeline("text-classification", self.model_name)
        for key, value in features.items():
            classifier= self.my_pipeline(self.model_name[language])
            results = classifier(value,max_length=512,truncation=True)
            joy = 0.0
            sadness = 0.0
            fear = 0.0
            anger = 0.0
            joy_absolute = 0
            sadness_absolute=0
            fear_absolute =0
            anger_absolute =0
            if results[0]['label'] == 'joy':
                joy = results[0]['score']
                joy_absolute = 1 if results[0]['score'] >= 0.5 else 0
            if results[0]['label'] == 'sadness':
                sadness = - results[0]['score']
                sadness_absolute = 1 if results[0]['score'] >= 0.5 else 0
            if results[0]['label'] == 'fear':
                fear = - results[0]['score']
                fear_absolute = 1 if results[0]['score'] >= 0.5 else 0
            if results[0]['label'] == 'anger':
                anger = - results[0]['score']
                anger_absolute = 1 if results[0]['score'] >= 0.5 else 0
                
            result["joy"][key]={
                        "values" : {
                         "absolute": joy_absolute,   
                         "local_normalisation": round(joy,3),
                         "global_normalisation": None,
                        },
                        'descriptions': {
                              'absolute': {'en': '', 'it': ''},
                              'local_normalisation': {'en': '', 'it': ''},
                              'global_normalisation': {'en': None, 'it': None}
                        }
            }
            result["sadness"][key]={
                        "values" : {
                         "absolute": sadness_absolute,
                         "local_normalisation": round(sadness,3),
                         "global_normalisation": None,
                        },
                        'descriptions': {
                              'absolute': {'en': '', 'it': ''},
                              'local_normalisation': {'en': '', 'it': ''},
                              'global_normalisation': {'en': None, 'it': None}
                        }
            }
            result["fear"][key]={
                        "values" : {
                         "absolute": fear_absolute,
                         "local_normalisation": round(fear,3),
                         "global_normalisation": None,
                        },
                        'descriptions': {
                              'absolute': {'en': '', 'it': ''},
                              'local_normalisation': {'en': '', 'it': ''},
                              'global_normalisation': {'en': None, 'it': None}
                        }
            }
            result["anger"][key]={
                        "values" : {
                         "absolute": anger_absolute,
                         "local_normalisation": round(anger,3),
                         "global_normalisation": None,
                        },
                        'descriptions': {
                              'absolute': {'en': '', 'it': ''},
                              'local_normalisation': {'en': '', 'it': ''},
                              'global_normalisation': {'en': None, 'it': None}
                        }
            }

        return result

    def __get_emotion(self, language, title: str, content: str, phenomena):
        prediction = self.__prediction(language, title, content)
        result = prediction[phenomena]


        return result


    def get_emotion_joy(self,language, title, content):

        return self.__get_emotion(language, title, content, phenomena="joy")


    def get_emotion_sadness(self,language, title, content):

        return self.__get_emotion(language, title, content, phenomena="sadness")


    def get_emotion_fear(self,language, title, content):

        return self.__get_emotion(language, title, content, phenomena="fear")


    def get_emotion_anger(self,language, title, content):

        return self.__get_emotion(language, title, content, phenomena="anger")



if __name__ == '__main__':
    title="l'arresto è avvenuto alle 3 del pomeriggio, non se ne può più!"
    content='mi piace giocare anche se non con te'
    sentiment = Sentiment()
    print(json.dumps(sentiment.get_sentiment_positive("it",title,content)))
    print(json.dumps(sentiment.get_sentiment_negative("en",title,content)))

    emotion = Emotion()
    print(json.dumps(emotion.get_emotion_joy("en",title,content)))
    print(json.dumps(emotion.get_emotion_sadness("it",title,content)))
    print(json.dumps(emotion.get_emotion_fear("en",title,content)))
    print(json.dumps(emotion.get_emotion_anger("it",title,content)))

