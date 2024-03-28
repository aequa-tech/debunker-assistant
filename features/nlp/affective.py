import json
from functools import lru_cache
from transformers import pipeline

class Sentiment():
    """
    Class that implements sentiment analysis in a zero-shot fashion
    """
    def __init__(self):
        self.model_name = 'neuraly/bert-base-italian-cased-sentiment'

    @lru_cache(maxsize=32)
    def my_pipeline(self, model_name):
        classifier = pipeline("text-classification", model_name)
        return classifier

    def prediction(self, title: str, content: str):
        """
        input:
            @param title: str: string containing the title of a news
            @param content: str: string containing the textual content of a news
        output:
            - dictionary of the prediction in the form {'positive': 1, 'negative': -1, 'overall': 0.5}
        """
        result={
            "description" : "Sentiment Analysis reports the sentiment expressed in the text. A score near to 1 shows a general positive opinion, while a score near to -1 shows a general negative opinion."
        }

        features = {"title" : title, "content" : content}
        classifier=self.my_pipeline(self.model_name)

        for key, value in features.items():
            results = classifier(value)
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
            
            result[key]={
                        "positive":
                        { "description" : f"The score of positive sentiment expressed in the text.",
                         "absolute": positivity_absolute,   
                         "local_normalisation": round(positivity,3),
                         "global_normalisation": None,
                        },
                        "negative":
                        { "description" : f"The score of negative sentiment expressed in the text.",
                         "absolute": negativity_absolute,   
                         "local_normalisation": round(negativity,3),
                         "global_normalisation": None,
                        },
                        # "overall":                                                
                        # { "description" : f"The overall score of sentiment expressed in the text.",
                        #  "absolute": None,
                        #  "local_normalization": round(overall,3),
                        #  "global_normalisation": None,
                        # }
            }

        return result

class Emotion():
    """
    Class that implements sentiment analysis in a zero-shot fashion
    """
    def __init__(self):
        self.model_name = "MilaNLProc/feel-it-italian-emotion"

    @lru_cache(maxsize=32)
    def my_pipeline(self, model_name):
        classifier = pipeline("text-classification", model_name)
        return classifier

    def prediction(self, title: str, content: str):
        """
        input:
            @param title: str: string containing the title of a news
            @param content: str: string containing the textual content of a news
        output:
            - dictionary of the prediction in the form {'positive': 1, 'negative': -1, 'overall': 0.5}
        """
        result={
            "description" : "Emotion Analysis reports the set of emotions expressed in the text. A score near to 1 shows the expression of an intense emotion, while a score near to 0 shows a low intensity."
        }

        features = {"title" : title, "content" : content}
        classifier=self.my_pipeline(self.model_name)

        for key, value in features.items():
            results = classifier(value)
            print(key, results)
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
                
            result[key]={
                        "joy":
                        { "description" : f"The score of joy emotion expressed in the text.",
                         "absolute": joy_absolute,   
                         "local_normalisation": round(joy,3),
                         "global_normalisation": None,
                        },
                        "sadness":
                        { "description" : f"The score of negative sentiment expressed in the text.",
                         "absolute": sadness_absolute,   
                         "local_normalisation": round(sadness,3),
                         "global_normalisation": None,
                        },
                        "fear":                                                
                        { "description" : f"The overall score of sentiment expressed in the text.",
                         "absolute": fear_absolute,
                         "local_normalization": round(fear,3),
                         "global_normalisation": None,
                        },
                        "anger":                                                
                        { "description" : f"The overall score of sentiment expressed in the text.",
                         "absolute": anger_absolute,
                         "local_normalization": round(anger,3),
                         "global_normalisation": None,
                        } }

        return result


if __name__ == '__main__':
    sentiment = Sentiment()
    emotion = Emotion()
    
    # title="l'arresto è avvenuto alle 3 del pomeriggio, poverino"
    # content='mi piace giocare anche se mi stanca'
    title="l'arresto è avvenuto alle 3 del pomeriggio, non se ne può più!"
    content='mi piace giocare anche se non con te'
    
    import time

    # Start timer
    start_time = time.perf_counter()

    print(json.dumps(emotion.prediction(title, content), indent=4))
    # print(json.dumps(sentiment.prediction(title, content), indent=4))
    exit()
    # End timer
    end_time = time.perf_counter()

    # Calculate elapsed time
    elapsed_time = end_time - start_time
    print("Elapsed time: ", elapsed_time)