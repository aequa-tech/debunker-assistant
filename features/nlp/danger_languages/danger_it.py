from transformers import  AutoTokenizer, pipeline
import torch
from transformers import AutoModelForSequenceClassification
from safetensors.torch import load_file
import io
from peft import LoraConfig, get_peft_model
from peft import set_peft_model_state_dict
import numpy as np
from functools import lru_cache
import json
import os.path

class Irony_it():
    """
    Class that implements the detection of irony/sarcasm.
    The detection of this pragmatic phenomenon in the texts is obtained thanks to a fine-tuned model starting from Language Models available for Italian.
    """
    def __init__(self):

        self.language_model = "m-polignano-uniba/bert_uncased_L-12_H-768_A-12_italian_alb3rt0"
        self.irony_model= "aequa-tech/irony-it"

    @lru_cache(maxsize=32)
    def __my_pipeline(self, language_model, model_name):
        tokenizer = AutoTokenizer.from_pretrained(language_model) 
        classifier = pipeline("text-classification", model=model_name, tokenizer=tokenizer)
        return classifier
   
    def get_irony(self, title: str, content: str):
        """
        input:
            @param title: str: string containing the title of a news
            @param content: str: string containing the textual content of a news
        output:
            - dictionary of the prediction: the absolute value = 1/0, local = logit coming from sigmoid function, global = None
        """
        
        result=dict()

        features = {"title" : title, "content" : content}
        classifier=self.__my_pipeline(self.language_model, self.irony_model)

        for key, value in features.items():
        
            score = classifier(value, truncation=True)[0]
            # print(score)
            absolute = 1 if score['score'] > 0.5 else 0
            local = score['score']
            # print(absolute, local)
        
            result[key]={ "values":{
                         "absolute": round(absolute,3),   
                         "local": round(local,3),
                         "global": None,
                        }}
        return result

class Flame_it():
    """
    Class that implements the detection of flame.
    The detection of this pragmatic phenomenon in the texts is obtained thanks to a fine-tuned model starting from Language Models available for Italian.
    """
    def __init__(self):

        self.language_model = "m-polignano-uniba/bert_uncased_L-12_H-768_A-12_italian_alb3rt0"
        self.flame_model= "aequa-tech/flame-it"

    @lru_cache(maxsize=32)
    def __my_pipeline(self, language_model, model_name):
        tokenizer = AutoTokenizer.from_pretrained(language_model) 
        classifier = pipeline("text-classification", model=model_name, tokenizer=tokenizer)
        return classifier
        
    def get_flame(self, title: str, content: str):
        """
        input:
            @param title: str: string containing the title of a news
            @param content: str: string containing the textual content of a news
        output:
            - dictionary of the prediction: the absolute value = 1/0, local = logit coming from sigmoid function, global = None
        """
        classifier=self.__my_pipeline(self.language_model, self.flame_model)
        result=dict()

        features = {"title" : title, "content" : content}
        for key, value in features.items():
        
            score = classifier(value, truncation=True)[0]
            # print(score)
            absolute = 1 if score['score'] > 0.5 else 0
            local = score['score']
            # print(absolute, local)
        
            result[key]={ "values":{
                         "absolute": round(absolute,3),   
                         "local": round(local,3),
                         "global": None,
                        }}
        return result

class Stereotype_it():
    """
    Class that implements the detection of stereotypes.
    The detection of this pragmatic phenomenon in the texts is obtained thanks to a fine-tuned model starting from Language Models available for Italian.
    """
    def __init__(self):

        self.language_model = "m-polignano-uniba/bert_uncased_L-12_H-768_A-12_italian_alb3rt0"
        self.stereotype_model= "aequa-tech/stereotype-it"

    @lru_cache(maxsize=32)
    def __my_pipeline(self, language_model, model_name):
        tokenizer = AutoTokenizer.from_pretrained(language_model) 
        classifier = pipeline("text-classification", model=model_name, tokenizer=tokenizer)
        return classifier
        
    def get_stereotype(self,  title: str, content: str):
        """
        input:
            @param title: str: string containing the title of a news
            @param content: str: string containing the textual content of a news
        output:
            - dictionary of the prediction: the absolute value = 1/0, local = logit coming from sigmoid function, global = None
        """
        
        result=dict()

        features = {"title" : title, "content" : content}
        classifier=self.__my_pipeline(self.language_model, self.stereotype_model)

        for key, value in features.items():
        
            score = classifier(value, truncation=True)[0]
            #print(score)
            absolute = 1 if score['score'] > 0.5 else 0
            local = score['score']
            # print(absolute, local)
        
            result[key]= { "values":{
                         "absolute": round(absolute,3),   
                         "local": round(local,3),
                         "global": None,
                        }}
        return result

if __name__ == '__main__':
    irony = Irony_it()
    flame = Flame_it()
    stereotype = Stereotype_it()

    txt = "io sono io"
    c = 'domani li sento'
    print(irony.get_irony(txt, c))


   # ...

