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
        self.model_name={}
        self.classifier={}
        self.model_name["it"] = 'neuraly/bert-base-italian-cased-sentiment'
        self.model_name["en"] = 'neuraly/bert-base-italian-cased-sentiment'

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
    def __explaination(self, language: str, title: str, content: str):
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
        
        for key, value in features.items():
            if key != 'title':
                continue
            print(value)
            classifier = self.__my_pipeline(self.model_name[language])
            results = classifier(value,truncation=True)
            # print(results)

            shap_model = shap.models.TransformersPipeline(classifier, rescale_to_logits=False)
            explainer = shap.Explainer(shap_model)
            shap_values = explainer([value])
            # print(shap_values) 

            word_p, weight_p = self.__max(shap_values, 'positive')
            word_n, weight_n = self.__max(shap_values, 'negative')
            
            result['positive'][key]={
                           "values" : {

                               "word": word_p,
                               "local_normalisation": round(weight_p, 3),
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

                               "word": word_n,
                               "local_normalisation": round(weight_n, 3),
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
        explaination = self.__explaination(language, title, content)
        result = explaination[phenomena]
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
    def __explaination(self, language, title: str, content: str):
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
                "en" : "The score of presence of fear expressed in the text.",
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
        
        for key, value in features.items():
            if key != 'title':
                continue
            print(value)
            classifier = self.__my_pipeline(self.model_name[language])
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
                         "word": word_s,
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
                         "word": word_f,
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
                         "word": word_a,
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
        explaination = self.__explaination(language, title, content)
        result = explaination[phenomena]
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
    print(json.dumps(sentiment.get_sentiment_negative("it",title,content)))
    # print(json.dumps(sentiment.get_sentiment_negative("en",title,content)))

    emotion = Emotion()
    # print(json.dumps(emotion.get_emotion_joy("en",title,content)))
    print(json.dumps(emotion.get_emotion_sadness("it",title,content)))
    # print(json.dumps(emotion.get_emotion_fear("en",title,content)))
    print(json.dumps(emotion.get_emotion_anger("it",title,content)))

