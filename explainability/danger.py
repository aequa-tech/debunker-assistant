from transformers import  AutoTokenizer, pipeline, AutoModelForSequenceClassification
import torch
from safetensors.torch import  load_file
import io
from peft import LoraConfig, get_peft_model
from peft import set_peft_model_state_dict
import numpy as np
from functools import lru_cache
import json
import shap

model_name = {}
model_name["it"] = 'm-polignano-uniba/bert_uncased_L-12_H-768_A-12_italian_alb3rt0'
model_name["en"] = 'm-polignano-uniba/bert_uncased_L-12_H-768_A-12_italian_alb3rt0'
tokenizer = {}
tokenizer["it"] = AutoTokenizer.from_pretrained(model_name["it"])
tokenizer["en"] = AutoTokenizer.from_pretrained(model_name["en"])

class Irony():
    """
    Class that implements the detection of irony/sarcasm.
    The detection of this pragmatic phenomenon in the texts is obtained thanks to a fine-tuned model starting from Language Models available for Italian.
    """
    def __init__(self):

        self.lora_model = {}
        self.lora_model["it"] = 'aequa-tech/lora-irony'
        self.lora_model["en"] = 'aequa-tech/lora-irony'

    @lru_cache(maxsize=32)
    def __my_pipeline(self, lora_model, model_name, tokenizer):
        model = AutoModelForSequenceClassification.from_pretrained(lora_model,num_labels=2)
        classifier = pipeline("text-classification", model=model_name, tokenizer=tokenizer, top_k=None)
        return classifier
    
    def __max(self, data,label):
        max = np.max(data[:,:,label].values)
        index = np.where(data[:,:,label].values == max)[1][0]
        word = np.take(data[:,:,label].data, index)
        return word.strip(), max
        
    def get_explaination(self, language, title: str, content: str):
        """
        input:
            @param title: str: string containing the title of a news
            @param content: str: string containing the textual content of a news
        output:
            - dictionary of the prediction: the absolute value = 1/0, local_normalisation = logit coming from sigmoid function, global_normalisation = None
        """
        result={
            "description" : "Prediction of irony in the text. A score near to 1 indicates the presence of irony, while a negative score or a score near to 0 the absence of irony."
        }
        
        features = {"title" : title, "content" : content}

        for key, value in features.items():
            if key != 'title':
                continue
            print(value)
            classifier = self.__my_pipeline(self.lora_model[language], model_name[language], tokenizer[language])
            results = classifier(value,truncation=True)
            print(results)

            shap_model = shap.models.TransformersPipeline(classifier, rescale_to_logits=False)
            explainer = shap.Explainer(shap_model)
            shap_values = explainer([value])
            # print(shap_values) 

            word_p, weight_p = self.__max(shap_values, 'LABEL_1') #get span only for positive class
            # word_n, weight_n = self.__max(shap_values, 'LABEL_0')
            print(word_p, weight_p)
            
            result[key]={
                        "values":
                        {
                         "word": word_p,
                         "local": round(weight_p, 3),
                         "global": None,
                        },
                        'descriptions': {
                              'absolute': {'en': '', 'it': ''},
                              'local': {'en': '', 'it': ''},
                              'global': {'en': None, 'it': None}
                        }
            }
        return result

class Flame():
    """
    Class that implements the detection of flame.
    The detection of this pragmatic phenomenon in the texts is obtained thanks to a fine-tuned model starting from Language Models available for Italian.
    """
    def __init__(self):

        self.lora_model = {}
        self.lora_model["it"] = 'aequa-tech/lora-flame'
        self.lora_model["en"] = 'aequa-tech/lora-flame'

    @lru_cache(maxsize=32)
    def __my_pipeline(self, lora_model, model_name, tokenizer):
        model = AutoModelForSequenceClassification.from_pretrained(lora_model,num_labels=2)
        classifier = pipeline("text-classification", model=model_name, tokenizer=tokenizer, top_k=None)
        return classifier
    
    def __max(self, data,label):
        max = np.max(data[:,:,label].values)
        index = np.where(data[:,:,label].values == max)[1][0]
        word = np.take(data[:,:,label].data, index)
        return word.strip(), max
        
    def get_explaination(self, language, title: str, content: str):
        """
        input:
            @param title: str: string containing the title of a news
            @param content: str: string containing the textual content of a news
        output:
            - dictionary of the prediction: the absolute value = 1/0, local_normalisation = logit coming from sigmoid function, global_normalisation = None
        """

        result={
            "description" : "Prediction of flaem in the text. A score near to 1 indicates the presence of irony, while a negative score or a score near to 0 the absence of irony."
        }

        features = {"title" : title, "content" : content}

        for key, value in features.items():
            if key != 'title':
                continue
            print(value)
            classifier = self.__my_pipeline(self.lora_model[language], model_name[language], tokenizer[language])
            results = classifier(value,truncation=True)
            print(results)

            shap_model = shap.models.TransformersPipeline(classifier, rescale_to_logits=False)
            explainer = shap.Explainer(shap_model)
            shap_values = explainer([value])
            # print(shap_values) 

            word_p, weight_p = self.__max(shap_values, 'LABEL_1') #get span only for positive class
            # word_n, weight_n = self.__max(shap_values, 'LABEL_0')
            print(word_p, weight_p)
            
            result[key]={
                        "values":
                        {
                         "word": word_p,
                         "local": round(weight_p, 3),
                         "global": None,
                        },
                        'descriptions': {
                              'absolute': {'en': '', 'it': ''},
                              'local': {'en': '', 'it': ''},
                              'global': {'en': None, 'it': None}
                        }
            }
        return result

class Stereotype():
    """
    Class that implements the detection of stereotypes.
    The detection of this pragmatic phenomenon in the texts is obtained thanks to a fine-tuned model starting from Language Models available for Italian.
    """
    def __init__(self):

        self.lora_model = {}
        self.lora_model["it"] = 'aequa-tech/lora-stereotype'
        self.lora_model["en"] = 'aequa-tech/lora-stereotype'

    @lru_cache(maxsize=32)
    def __my_pipeline(self, lora_model, model_name, tokenizer):
        model = AutoModelForSequenceClassification.from_pretrained(lora_model,num_labels=2)
        classifier = pipeline("text-classification", model=model_name, tokenizer=tokenizer, top_k=None)
        return classifier
    
    def __max(self, data,label):
        max = np.max(data[:,:,label].values)
        index = np.where(data[:,:,label].values == max)[1][0]
        word = np.take(data[:,:,label].data, index)
        return word.strip(), max
        
    def get_explaination(self, language, title: str, content: str):
        """
        input:
            @param title: str: string containing the title of a news
            @param content: str: string containing the textual content of a news
        output:
            - dictionary of the prediction: the absolute value = 1/0, local_normalisation = logit coming from sigmoid function, global_normalisation = None
        """

        result={
            "description" : "Prediction of stereotypes in the text. A score near to 1 indicates the presence of irony, while a negative score or a score near to 0 the absence of irony."
        }

        features = {"title" : title, "content" : content}

        for key, value in features.items():
            if key != 'title':
                continue
            print(value)
            classifier = self.__my_pipeline(self.lora_model[language], model_name[language], tokenizer[language])
            results = classifier(value,truncation=True)
            print(results)

            shap_model = shap.models.TransformersPipeline(classifier, rescale_to_logits=False)
            explainer = shap.Explainer(shap_model)
            shap_values = explainer([value])
            # print(shap_values) 

            word_p, weight_p = self.__max(shap_values, 'LABEL_1') #get span only for positive class
            # word_n, weight_n = self.__max(shap_values, 'LABEL_0')
            print(word_p, weight_p)
            
            result[key]={
                        "values":
                        {
                         "word": word_p,
                         "local": round(weight_p, 3),
                         "global": None,
                        },
                        'descriptions': {
                              'absolute': {'en': '', 'it': ''},
                              'local': {'en': '', 'it': ''},
                              'global': {'en': None, 'it': None}
                        }
            }
        return result

if __name__ == '__main__':

    title="l'arresto è avvenuto alle 3 del pomeriggio, poverino"
    content='era un albanese, dobbiamo continuare con questo processo di integrazione?'

    print("IRONY")
    irony = Irony()
    print(json.dumps(irony.get_explaination("it",title, content), indent=4))
    # print(json.dumps(irony.get_explaination("en",title, content), indent=4))

    print("FLAME")
    flame = Flame()
    print(json.dumps(flame.get_explaination("it",title, content), indent=4))
    # print(json.dumps(flame.get_flame("en",title, content), indent=4))

    print("STEREOTYPE")
    stereotypes = Stereotype()
    print(json.dumps(stereotypes.get_explaination("it",title, content), indent=4))
    # print(json.dumps(stereotypes.get_stereotype("en",title, content), indent=4))

