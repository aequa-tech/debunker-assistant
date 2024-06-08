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
    def __init__(self,language):

        if language=="en":
            self.sentiment_model = 'neuraly/bert-base-italian-cased-sentiment'
            self.affective_model = "MilaNLProc/feel-it-italian-emotion"
            self.sentiment = ['positive', 'negative']
            self.affective = ['anger', 'fear', 'joy', 'sadness']

            self.flame_model = 'facebook/roberta-hate-speech-dynabench-r4-target'
            self.irony_model = 'cardiffnlp/twitter-roberta-base-irony'
            self.stereotype_model = 'aequa-tech/stereotype-it'
            self.stereotype_model = 'cardiffnlp/twitter-roberta-base-irony' #da sistemare
            self.danger = ['flame', 'irony', 'stereotype']
        else:
            self.sentiment_model = 'neuraly/bert-base-italian-cased-sentiment'
            self.affective_model = "MilaNLProc/feel-it-italian-emotion"
            self.sentiment = ['positive', 'negative']
            self.affective = ['anger', 'fear', 'joy', 'sadness']

            self.flame_model = 'aequa-tech/irony-it'
            self.irony_model = 'aequa-tech/flame-it'
            self.stereotype_model = 'aequa-tech/stereotype-it'
            self.danger = ['flame', 'irony', 'stereotype']

    @lru_cache(maxsize=32)
    def __my_pipeline(self, model_name):
        print(model_name)
        classifier = pipeline("text-classification", model=model_name, top_k=None)
        return classifier

    def __max(self, data,label):
        label=1 #da rivedere
        max = np.max(data[:,:,label].values)
        index = np.where(data[:,:,label].values == max)[1][0]
        word = np.take(data[:,:,label].data, index)
        return word.strip(), max
    
    @lru_cache(maxsize=32)
    def __explaination(self, model, title: str, content):
        """
        input:
            @param title: str: string containing the title of a news
            @param content: str: string containing the textual content of a news
        output:
            - dictionary of the prediction in the form {'positive': 1, 'negative': -1, 'overall': 0.5}
        """

        features = {"title" : title}#"content" : content}
        
        for key, value in features.items():
            print(value)
            print(type(value),model)
            classifier = self.__my_pipeline(model)
            results = classifier(value,truncation=True)

            #classifier.model.config.label2id=classifier.model.config.id2label.copy()
            #print(results)
            classifier.model.config.label2id={v: k for k, v in enumerate([x['label'] for x in results[0]])}
            #classifier.model.config.id2label.update({k: v for k, v in enumerate([x['label'] for x in results[0]])})

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
    def get_sentiment(self, title: str, content, phenomena):
        if phenomena in self.sentiment:
            model = self.sentiment_model
        else:
            model = self.affective_model

        explaination = self.__explaination( model,title)
        result = self.__extract_word(explaination,phenomena)
        
        return result
    
    @lru_cache(maxsize=32)
    def get_danger(self, title: str, content, phenomena):
        if phenomena =='stereotype':
            model = self.stereotype_model
        elif phenomena=='flame':
            model = self.flame_model
        else:
            model = self.irony_model

        explaination = self.__explaination( model,title,content)
        result = self.__extract_word(explaination,phenomena)
        
        return result

    '''def get_sentiment_positive(self,title):
        return self.__get_sentiment(title, phenomena="positive")

    def get_sentiment_negative(self,title):
        return self.__get_sentiment(title, phenomena="negative")'''


class Affective:
    def __init__(self):
        self.affective_explanation_it = Explainer("it")
        self.affective_explanation_en = Explainer("en")
        

    def affective_explanation(self,title, content, language):
        d = dict()
        for item in ['positive','negative','sadness','fear','joy','anger']:
            if language=="it":
                sent = self.affective_explanation_it.get_sentiment(title, content, item)
                d[item] = sent
            else:
                sent = self.affective_explanation_en.get_sentiment(title, content, item)
                d[item] = sent
        return d

class Danger:
    def __init__(self):
        self.darget_explanation_it = Explainer("it")
        self.darget_explanation_en = Explainer("en")


    def danger_explanation(self,title, content, language):
        d = dict()
        for item in ['flame','stereotype','irony']:
            if language=="it":
                sent = self.darget_explanation_it.get_danger(title, content, item)
                d[item] = sent
            else:
                sent = self.darget_explanation_en.get_danger(title, content, item)
                d[item] = sent
        return d
        



if __name__ == "__main__":
    explainer_danger=Danger()
    result=explainer_danger.danger_explanation("questo è un titolo di prova","prova","en")
    print(result)

