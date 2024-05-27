import json
from functools import lru_cache
from transformers import pipeline, AutoTokenizer
import shap
import numpy as np

class Explainer:
    """
    Class that implements sentiment analysis in a zero-shot fashion
    """

    @lru_cache(maxsize=32)
    def __init__(self):
        self.sentiment_model = 'neuraly/bert-base-italian-cased-sentiment'
        self.affective_model = "MilaNLProc/feel-it-italian-emotion"
        self.sentiment = ['positive','negative']
        self.affective = ['anger','fear','joy','sadness']

        self.flame_model = ''
        self.irony_model = ''
        self.stereotype_model = ''
        self.danger = ['flame','irony','stereotype']

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
    def __explaination(self, model, title: str):
        """
        input:
            @param title: str: string containing the title of a news
            @param content: str: string containing the textual content of a news
        output:
            - dictionary of the prediction in the form {'positive': 1, 'negative': -1, 'overall': 0.5}
        """

        features = {"title" : title}
        
        for key, value in features.items():
            print(value)
            print(type(value))
            classifier = self.__my_pipeline(model)
            results = classifier(value,truncation=True)
            
            shap_model = shap.models.TransformersPipeline(classifier, rescale_to_logits=False)
            explainer = shap.Explainer(shap_model)
            shap_values = explainer([value])

        return shap_values
    
    def __extract_word(self,shap_values,phenomena : str):

        word, prob = self.__max(shap_values, phenomena)
            
        result ={
                               "token": word,
                               "probability": round(prob, 3)
                          }

        return result
    
    @lru_cache(maxsize=32)
    def get_sentiment(self, title: str, phenomena):
        if phenomena in self.sentiment:
            model = self.sentiment_model
        else:
            model = self.affective_model

        explaination = self.__explaination( model,title)
        result = self.__extract_word(explaination,phenomena)
        
        return result
    
    @lru_cache(maxsize=32)
    def get_danger(self, title: str, phenomena):
        if phenomena =='stereotype':
            model = self.stereotype_model
        elif phenomena=='flame':
            model = self.flame_model
        else:
            model = self.irony_model

        explaination = self.__explaination( model,title)
        result = self.__extract_word(explaination,'LABEL_1')
        
        return result

    '''def get_sentiment_positive(self,title):
        return self.__get_sentiment(title, phenomena="positive")

    def get_sentiment_negative(self,title):
        return self.__get_sentiment(title, phenomena="negative")'''


class Affective:
    def __init__(self):
        self.sentiment = Explainer()
        

    def affective_explanation(self,title):
        d = dict()
        for item in ['positive','negative','sadness','fear','joy','anger']:
            sent = self.sentiment.get_sentiment(title,item)
            d[item] = sent
        return d

class Danger:
    def __init__(self):
        self.sentiment = Explainer()
        

    def danger_explanation(self,title):
        d = dict()
        for item in ['flame','stereotype','irony']:
            sent = self.sentiment.get_danger(title,item)
            d[item] = sent
        return d
        

