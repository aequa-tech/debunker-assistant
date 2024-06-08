import json
from functools import lru_cache
from transformers import pipeline, AutoTokenizer
import shap
import numpy as np

class Sentiment():
    """
    Class that implements sentiment analysis in a zero-shot fashion
    """
    def __init__(self):
        self.model_name = 'neuraly/bert-base-italian-cased-sentiment'

    @lru_cache(maxsize=32)
    def __my_pipeline(self, model_name):
        classifier = pipeline("text-classification", model=model_name, top_k=None)
        return classifier

    def __max(self, data,label):
        max = np.max(data[:,:,label].values)
        print(data[:,:,label])
        index = np.where(data[:,:,label].values == max)[1][0]
        word = np.take(data[:,:,label].data, index)
        return word.strip(), max
    
    @lru_cache(maxsize=32)
    def __explaination(self, title: str, content: str):
        """
        input:
            @param title: str: string containing the title of a news
            @param content: str: string containing the textual content of a news
        output:
            - dictionary of the prediction in the form {'positive': 1, 'negative': -1, 'overall': 0.5}
        """
        result={
            'positive' : {

                'description': 'The score of positive sentiment expressed in the text.',


            },
            'negative' :{
                'description': 'The score of negative sentiment expressed in the text.'

             }
        }

        features = {"title" : title, "content" : content}
        
        for key, value in features.items():
            if key != 'title':
                continue
            print(value)
            classifier = self.__my_pipeline(self.model_name)
            results = classifier(value,truncation=True)
            print(results)
            shap_model = shap.models.TransformersPipeline(classifier, rescale_to_logits=False)
            explainer = shap.Explainer(shap_model)
            shap_values = explainer([value])
            print(shap_values) 
            
            word_p, weight_p = self.__max(shap_values, 'positive')
            word_n, weight_n = self.__max(shap_values, 'negative')
            
            result['positive'][key]={
                           "values" : {

                               "word": word_p,
                               "local": round(weight_p, 3),
                               "global": None,
                           },

                          'descriptions': {
                              'absolute': '',
                              'local':  '',
                              'global': None
                          }
            }

            result['negative'][key]={
                           "values" : {

                               "word": word_n,
                               "local": round(weight_n, 3),
                               "global": None,
                           },

                          'descriptions': {
                              'absolute':   '',
                              'local': '',
                              'global':  None
                          }
            }

        return result

    def __get_sentiment(self,  title: str, content: str, phenomena):
        explaination = self.__explaination( title, content)
        
        result = explaination[phenomena]
        print(result)
        return result

    def get_sentiment_positive(self,title, content):
        return self.__get_sentiment(title, content, phenomena="positive")

    def get_sentiment_negative(self,title, content):
        return self.__get_sentiment(title, content, phenomena="negative")

class Emotion():
    """
    Class that implements sentiment analysis in a zero-shot fashion
    """
    def __init__(self):
        self.model_name ={}
        self.model_name["it"] = "MilaNLProc/feel-it-italian-emotion"
        self.model_name["en"] = "MilaNLProc/feel-it-italian-emotion"

    @lru_cache(maxsize=32)
    def __my_pipeline(self, model_name):
        classifier = pipeline("text-classification", model=model_name, top_k=None)
        return classifier

    def __max(self, data,label):
        max = np.max(data[:,:,label].values)
        index = np.where(data[:,:,label].values == max)[1][0]
        word = np.take(data[:,:,label].data, index)
        return word.strip(), max
        
    @lru_cache(maxsize=32)
    def __explaination(self, title: str, content: str):
        """
        input:
            @param title: str: string containing the title of a news
            @param content: str: string containing the textual content of a news
        output:
            - dictionary of the prediction of each emotion
        """
        result={

            "joy" : {
                "description" : "The score of presence of joy expressed in the text.",

            },
            "sadness" : {
                "description" : "The score of presence of sadness expressed in the text.",
            },
            "fear" :  {
                "description" : "The score of presence of fear expressed in the text.",
            },
            "anger" :  {
                "description" : "The score of presence of anger expressed in the text.",

            },

        }

        features = {"title" : title, "content" : content}
        
        for key, value in features.items():
            if key != 'title':
                continue
            print(value)
            classifier = self.__my_pipeline(self.model_name)
            results = classifier(value,truncation=True)
            # print(results)

            shap_model = shap.models.TransformersPipeline(classifier, rescale_to_logits=False)
            explainer = shap.Explainer(shap_model)
            shap_values = explainer([value])
            # print(shap_values) 

            word_j, joy = self.__max(shap_values, 'joy')
            word_s, sadness = self.__max(shap_values, 'sadness')
            word_f, fear = self.__max(shap_values, 'fear')
            word_a, anger = self.__max(shap_values, 'anger')  
                
            result["joy"][key]={
                        "values" : {
                         "word": word_j,   
                         "local": round(joy,3),
                         "global": None,
                        },
                        'descriptions': {
                              'absolute':  '',
                              'local': '',
                              'global':  None
                        }
            }
            result["sadness"][key]={
                        "values" : {
                         "word": word_s,
                         "local": round(sadness,3),
                         "global": None,
                        },
                        'descriptions': {
                              'absolute': '',
                              'local': '',
                              'global': None
                        }
            }
            result["fear"][key]={
                        "values" : {
                         "word": word_f,
                         "local": round(fear,3),
                         "global": None,
                        },
                        'descriptions': {
                              'absolute': '',
                              'local': '',
                              'global': None
                        }
            }
            result["anger"][key]={
                        "values" : {
                         "word": word_a,
                         "local": round(anger,3),
                         "global": None,
                        },
                        'descriptions': {
                              'absolute': '',
                              'local': '',
                              'global': None
                        }
            }

        return result

    def __get_emotion(self,  title: str, content: str, phenomena):
        explaination = self.__explaination( title, content)
        result = explaination[phenomena]
        return result

    def get_emotion_joy(self, title, content):
        return self.__get_emotion(title, content, phenomena="joy")

    def get_emotion_sadness(self,title, content):
        return self.__get_emotion( title, content, phenomena="sadness")

    def get_emotion_fear(self,title, content):
        return self.__get_emotion( title, content, phenomena="fear")

    def get_emotion_anger(self,title, content):
        return self.__get_emotion( title, content, phenomena="anger")

if __name__ == '__main__':
    ...

