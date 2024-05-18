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
        #print(data[:,:,label])
        index = np.where(data[:,:,label].values == max)[1][0]
        word = np.take(data[:,:,label].data, index)
        return word.strip(), max
    
    @lru_cache(maxsize=32)
    def __explaination(self, title: str,phenomena):
        phenomena = phenomena.split('|')
        """
        input:
            @param title: str: string containing the title of a news
            @param content: str: string containing the textual content of a news
        output:
            - dictionary of the prediction in the form {'positive': 1, 'negative': -1, 'overall': 0.5}
        """

        features = {"title" : title}
        
        for key, value in features.items():
            
            classifier = self.__my_pipeline(self.model_name)
            results = classifier(value,truncation=True)
            
            shap_model = shap.models.TransformersPipeline(classifier, rescale_to_logits=False)
            explainer = shap.Explainer(shap_model)
            shap_values = explainer([value])
             
            
            results = list()
            for phenomenon in phenomena:

                word, prob = self.__max(shap_values, phenomenon)
             
                
                result={                         

                                "token": word,
                                "probability": round(prob, 3)
                            }
                results.append(result)

        return results

    def get_sentiment(self,  title: str, phenomena):
        explaination = self.__explaination( title,phenomena)
        
        return explaination

    '''def get_sentiment(self,title,phenomena)
    def get_sentiment_positive(self,title):
        return self.__get_sentiment(title, phenomena="positive")

    def get_sentiment_negative(self,title):
        return self.__get_sentiment(title, phenomena="negative")'''

class Emotion():
    """
    Class that implements sentiment analysis in a zero-shot fashion
    """
    def __init__(self):
        self.model_name ={}
        self.model_name = "MilaNLProc/feel-it-italian-emotion"

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
    def __explaination(self, title: str,phenomena):
        phenomena = phenomena.split('|')
        """
        input:
            @param title: str: string containing the title of a news
            @param content: str: string containing the textual content of a news
        output:
            - dictionary of the prediction of each emotion
        """
        

        features = {"title" : title}
        
        for key, value in features.items():
            print(key,value)
            classifier = self.__my_pipeline(self.model_name)
            results = classifier(value,truncation=True)
            # print(results)

            shap_model = shap.models.TransformersPipeline(classifier, rescale_to_logits=False)
            explainer = shap.Explainer(shap_model)
            shap_values = explainer([value])
            # print(shap_values) 
            results = list()
            for phenomenon in phenomena:

                word, prob = self.__max(shap_values, phenomenon)
             
                
                result={                         

                                "token": word,
                                "probability": round(prob, 3)
                            }
                results.append(result)

        return results

    def get_emotion(self,  title: str, phenomena):
        explaination = self.__explaination(title,phenomena)
        
        return explaination

    '''def get_emotion_joy(self, title):
        return self.__get_emotion(title, phenomena="joy")

    def get_emotion_sadness(self,title):
        return self.__get_emotion( title, phenomena="sadness")

    def get_emotion_fear(self,title):
        return self.__get_emotion( title, phenomena="fear")

    def get_emotion_anger(self,title):
        return self.__get_emotion( title, phenomena="anger")'''


class Affective:
    def __init__(self):
        self.sentiment = Sentiment()
        self.emotions = Emotion()

    def affective_explanations(self,title):
        d = dict()
        sent_phen = ['positive','negative']
        aff_phen = ['anger','fear','joy','sadness']
        sentiment = self.sentiment.get_sentiment(title,phenomena='|'.join(sent_phen))
        affective = self.emotions.get_emotion(title,phenomena='|'.join(aff_phen))
        for i,item in enumerate(sentiment):
            d[sent_phen[i]] = item
        for i,item in enumerate(affective):
            d[aff_phen[i]] = item

        return d
        

