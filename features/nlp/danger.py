from transformers import  AutoTokenizer
import torch
from transformers import AutoModelForSequenceClassification
from safetensors.torch import  load_file
import io
from peft import LoraConfig, get_peft_model
from peft import set_peft_model_state_dict
import numpy as np
from functools import lru_cache
import json

class Irony():
    """
    Class that implements the detection of irony/sarcasm.
    The detection of this pragmatic phenomenon in the texts is obtained thanks to a fine-tuned model starting from Language Models available for Italian.
    """
    def __init__(self):
        self.model_name = 'm-polignano-uniba/bert_uncased_L-12_H-768_A-12_italian_alb3rt0'
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name, num_labels=2)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.lora_model = self.__model_lora()

    def __model_lora(self):
        """
        This method creates an instance of lora used in our fine-tuned model to reduce the parameters of Language Model (and weight of the final model).
        """
        config = LoraConfig(
            r=16,
            lora_alpha=32,
            target_modules=["query", "value"],
            lora_dropout=0.01,
            bias="none",
            task_type="classifier",
            modules_to_save=["classifier"]
        )

        lora_model = get_peft_model(self.model, config)
        return lora_model
   
    @lru_cache(maxsize=32)
    def my_tokenizer(self, text):
        tokenized = self.tokenizer.encode_plus(text,return_tensors='pt',max_length=512)
        feat = tokenized['input_ids']
        attention = tokenized['attention_mask']
        return feat, attention
        
    def get_irony(self, title: str, content: str):
        """
        input:
            @param title: str: string containing the title of a news
            @param content: str: string containing the textual content of a news
        output:
            - dictionary of the prediction: the absolute value = 1/0, local_normalisation = logit coming from sigmoid function, global_normalisation = None
        """
        cp = 'features/nlp/models/adapter_irony.safetensors'
        full_state_dict = load_file(cp)

        #adatta il modello generale con i pesi del task specifico
        set_peft_model_state_dict(self.lora_model, full_state_dict)
        self.lora_model.eval()
        sigmoid = torch.nn.Sigmoid()
        
        result={
            "description" : "Prediction of irony in the text. A score near to 1 indicates the presence of irony, while a negative score or a score near to 0 the absence of irony."
        }

        features = {"title" : title, "content" : content}

        for key, value in features.items():
            feat, attention = self.my_tokenizer(value)
        
            score = self.lora_model(input_ids=feat, attention_mask=attention)
            # print(score)
            score_sig = sigmoid(score['logits'].detach())
            absolute = torch.argmax(score_sig).item()
            # local = score['logits'][0,1].item() #non normalizzato e logit solo della classe positiva
            local = score_sig[0,1].item() # normalizzato con sigmoid e logit solo della classe positiva
            # print(score_sig, absolute, local)
        
            result[key]={
                        "values":
                        {
                         "absolute": round(absolute,3),   
                         "local_normalisation": round(local,3),
                         "global_normalisation": None,
                        },
                        'descriptions': {
                              'absolute': {'en': '', 'it': ''},
                              'local_normalisation': {'en': '', 'it': ''},
                              'global_normalisation': {'en': None, 'it': None}
                        }
            }
        return result

class Flame():
    """
    Class that implements the detection of flame.
    The detection of this pragmatic phenomenon in the texts is obtained thanks to a fine-tuned model starting from Language Models available for Italian.
    """
    def __init__(self):
        self.model_name = 'm-polignano-uniba/bert_uncased_L-12_H-768_A-12_italian_alb3rt0'
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name, num_labels=2)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.lora_model = self.__model_lora()

    def __model_lora(self):
        """
        This method creates an instance of lora used in our fine-tuned model to reduce the parameters of Language Model (and weight of the final model).
        """
        config = LoraConfig(
            r=16,
            lora_alpha=32,
            target_modules=["query", "value"],
            lora_dropout=0.01,
            bias="none",
            task_type="classifier",
            modules_to_save=["classifier"]
        )

        lora_model = get_peft_model(self.model, config)
        return lora_model
   
    @lru_cache(maxsize=32)
    def my_tokenizer(self, text):
        tokenized = self.tokenizer.encode_plus(text,return_tensors='pt',max_length=512)
        feat = tokenized['input_ids']
        attention = tokenized['attention_mask']
        return feat, attention
        
    def get_flame(self, title: str, content: str):
        """
        input:
            @param title: str: string containing the title of a news
            @param content: str: string containing the textual content of a news
        output:
            - dictionary of the prediction: the absolute value = 1/0, local_normalisation = logit coming from sigmoid function, global_normalisation = None
        """
        cp = 'features/nlp/models/adapter_hs.safetensors'
        full_state_dict = load_file(cp)

        #adatta il modello generale con i pesi del task specifico
        set_peft_model_state_dict(self.lora_model, full_state_dict)
        self.lora_model.eval()
        sigmoid = torch.nn.Sigmoid()
        
        result={
            "description" : "Prediction of flaem in the text. A score near to 1 indicates the presence of irony, while a negative score or a score near to 0 the absence of irony."
        }

        features = {"title" : title, "content" : content}

        for key, value in features.items():
            feat, attention = self.my_tokenizer(value)
        
            score = self.lora_model(input_ids=feat, attention_mask=attention)
            # print(score)
            score_sig = sigmoid(score['logits'].detach())
            absolute = torch.argmax(score_sig).item()
            local = score_sig[0,1].item() 
            # print(score_sig, absolute, local)
        
            result[key]={
                        "values":
                        {
                         "absolute": round(absolute,3),   
                         "local_normalisation": round(local,3),
                         "global_normalisation": None,
                        },
                        'descriptions': {
                              'absolute': {'en': '', 'it': ''},
                              'local_normalisation': {'en': '', 'it': ''},
                              'global_normalisation': {'en': None, 'it': None}
                        }
            }
        return result

class Stereotype():
    """
    Class that implements the detection of stereotypes.
    The detection of this pragmatic phenomenon in the texts is obtained thanks to a fine-tuned model starting from Language Models available for Italian.
    """
    def __init__(self):
        self.model_name = 'm-polignano-uniba/bert_uncased_L-12_H-768_A-12_italian_alb3rt0'
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name, num_labels=2)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.lora_model = self.__model_lora()

    def __model_lora(self):
        """
        This method creates an instance of lora used in our fine-tuned model to reduce the parameters of Language Model (and weight of the final model).
        """
        config = LoraConfig(
            r=16,
            lora_alpha=32,
            target_modules=["query", "value"],
            lora_dropout=0.01,
            bias="none",
            task_type="classifier",
            modules_to_save=["classifier"]
        )

        lora_model = get_peft_model(self.model, config)
        return lora_model
   
    @lru_cache(maxsize=32)
    def my_tokenizer(self, text):
        tokenized = self.tokenizer.encode_plus(text,return_tensors='pt',max_length=512)
        feat = tokenized['input_ids']
        attention = tokenized['attention_mask']
        return feat, attention
        
    def get_stereotype(self, title: str, content: str):
        """
        input:
            @param title: str: string containing the title of a news
            @param content: str: string containing the textual content of a news
        output:
            - dictionary of the prediction: the absolute value = 1/0, local_normalisation = logit coming from sigmoid function, global_normalisation = None
        """
        cp = 'features/nlp/models/adapter_stereotype.safetensors'
        full_state_dict = load_file(cp)

        #adatta il modello generale con i pesi del task specifico
        set_peft_model_state_dict(self.lora_model, full_state_dict)
        self.lora_model.eval()
        sigmoid = torch.nn.Sigmoid()
        
        result={
            "description" : "Prediction of stereotypes in the text. A score near to 1 indicates the presence of irony, while a negative score or a score near to 0 the absence of irony."
        }

        features = {"title" : title, "content" : content}

        for key, value in features.items():
            feat, attention = self.my_tokenizer(value)
        
            score = self.lora_model(input_ids=feat, attention_mask=attention)
            # print(score)
            score_sig = sigmoid(score['logits'].detach())
            absolute = torch.argmax(score_sig).item()
            local = score_sig[0,1].item()
            # print(score_sig, absolute, local)
        
            result[key]={
                        "values":
                        {
                         "absolute": round(absolute,3),   
                         "local_normalisation": round(local,3),
                         "global_normalisation": None,
                        },
                        'descriptions': {
                              'absolute': {'en': '', 'it': ''},
                              'local_normalisation': {'en': '', 'it': ''},
                              'global_normalisation': {'en': None, 'it': None}
                        }
            }
        return result

if __name__ == '__main__':

    title="l'arresto è avvenuto alle 3 del pomeriggio, poverino"
    content='era un albanese, dobbiamo continuare con questo processo di integrazione?'

    print("IRONY")
    irony = Irony()
    print(json.dumps(irony.get_irony(title, content), indent=4))

    print("FLAME")
    # flame = Flame()
    # print(json.dumps(flame.get_flame(title, content), indent=4))

    print("STEREOTYPE")
    # stereotypes = Stereotype()
    # print(json.dumps(stereotypes.get_stereotype(title, content), indent=4))

