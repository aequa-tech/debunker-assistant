"""

Main Characteristics of Informal Style Text
The informal style has the following characteristics:
- 1. It uses a personal style: the first and second person (“I” and “you”) and the active voice (e.g., “I have noticed that...”).
2. It uses short simple words and sentences (e.g., “latest”).
3. It uses contractions (e.g., “won’t”).
4. It uses many abbreviations (e.g., “TV”).
5. It uses many phrasal verbs in the text (e.g., “find out”).
6. Words that express rapport and familiarity are often used inspeech, such as “brother”, “buddy” and “man”.
7. It uses a subjective style, expressing opinions and feelings (e.g.,“pretty”, “I feel”).
8. It uses vague expressions, personal vocabulary and colloquialisms (slang words are accepted in spoken text, but not in written text(e.g., “wanna” = “want to”)).

Main Characteristics of Formal Style
The formal style has the following characteristics:
1. It uses an impersonal style: the third person (“it”, “he” and “she”) and often the passive voice (e.g.,“It has been noticed that...”).
2. It uses complex words and sentences to express complex points(e.g., “state-of-the-art”).
3. It does not use contractions.
4. It does not use many abbreviations, though there are some ab-breviations used in formal texts, such as titles with proper names(e.g., “Mr.”) or short names of methods in scientific papers (e.g.,“SVM”).
5. It uses appropriate and clear expressions, precise education, and business and technical vocabularies (Latin origin).
6. It uses polite words and formulae, such as “Please”, “Thank you”,“Madam” and “Sir”.7. It uses an objective style, citing facts and references to supportan argument.
8. It does not use vague expressions and slang words.

Sheikha, F. A., & Inkpen, D. (2012). Learning to Classify Documents According to Formal and Informal Style. Linguistic Issues in Language Technology, 8. https://doi.org/10.33011/lilt.v8i.1305

"""
import spacy
import hashlib
import random
import sys
import re

MAX_SIZE=10*1024*1024 #bytes

class Sensationalism:

    def __init__(self) -> None:
        self.nlp = spacy.load("it_core_news_lg") #['tok2vec', 'morphologizer', 'tagger', 'parser', 'lemmatizer', 'senter', 'attribute_ruler', 'ner']
        self.title_features={}
        self.content_features={}

    """It caches Spacy NLP objects called on text documents. The maximum size of the cache is defined by the constant MAX_SIZE."""
    def cached_features(self,title,content):

        hash_title   = hashlib.md5(title.encode('utf-8')).hexdigest()
        hash_content = hashlib.md5(title.encode('utf-8')).hexdigest()

        if hash_title in self.title_features:
            title_features = self.title_features[hash_title]
        else:
            title_features = self.title_features[hash_title] = self.nlp(title)

        while  len(self.title_features.keys())>0 and sys.getsizeof(self.title_features)>MAX_SIZE:
            key = random.choice(list(self.title_features.keys()))
            del self.title_features[key]

        if hash_content in self.content_features:
            content_features = self.content_features[hash_content]
        else:
            content_features = self.content_features[hash_content] = self.nlp(content)

        while  len(self.content_features.keys())>0 and sys.getsizeof(self.content_features)>MAX_SIZE:
            key = random.choice(list(self.content_features.keys()))
            del self.content_features[key]

        return title_features,content_features

    """It uses a personal style: the first and second person (“I” and “you”) and the active voice"""
    def use_of_personal_style(self, title, content):

        title_features,content_features=self.cached_features(title,content)

        variables=[title_features,content_features]
        variables_names=["title","content"]
        result={
            "description" : "One of the characteristics of the informal style is the use of a personal style, such as the use of first and second person (“I” and “you”) and the use of active voice (e.g., “I have noticed that...”)."
        }

        for i in range(0,len(variables)):

            personal_style=0
            not_personal_style=0
            for sent in variables[i].sents:
                for token in sent:
                    if token.pos_ == 'VERB':
                        #Mood = Ind | Number = Sing | Person = 1 | Tense = Pres | VerbForm = Fin
                        print(token.morph)
                        if token.morph.get("Person") in [['1'],['2']]:
                            personal_style+=1
                        else:
                            not_personal_style+=1

            ratio = personal_style/(personal_style+not_personal_style) if personal_style+not_personal_style>0 else 0
            result[variables_names[i]]={
                                            "personal style":
                                                { "description" : f"The numbers of times the first and second persons have been used.",
                                                  "value": personal_style,
                                                },
                                                "normalized personal style":
                                                { "description" : f"the fraction between the number of times the first and second persons have been used and the number of verbs",
                                                  "value" : ratio
                                                }
                                        }
        return result

    """It shouts or use other impolite  behaviors"""
    def use_of_uppercase_words(self, title, content):

        title_features,content_features=self.cached_features(title,content)

        variables=[title_features,content_features]
        variables_names=["title","content"]
        result={
            "description" : "One of the characteristics of the informal style is the use of capital letters used for shouting and other impolite or argumentative behaviors."
        }

        for i in range(0,len(variables)):

            uppercase=0
            not_uppercase=0
            for sent in variables[i].sents:
                for token in sent:
                    if len(token.text)>2:
                        if token.text not in [ent.text for ent in sent.ents]: # It excludes acronyms of organisations.
                            if token.text.isupper():
                                uppercase+=1
                            if token.text[1:].islower(): # it excludes the first char
                                not_uppercase+=1

            ratio = uppercase/(uppercase+not_uppercase) if uppercase+not_uppercase>0 else 0
            result[variables_names[i]]={
                                            "uppercase words":
                                                { "description" : f"The numbers of uppercase words.",
                                                  "value": uppercase,
                                                },
                                                "normalized uppercase words":
                                                { "description" : f"the fraction between the number of uppercase words and the number of words (the acronyms of organisations have been excluded).",
                                                  "value" : ratio
                                                }
                                        }
        return result


if __name__ == '__main__':
    sensationalism = Sensationalism()


    title='Io sto bene tu stai male NBC, CNN'
    content='Io sto bene tu stai male lui è stato picchiato CAZZOOO'

    print(sensationalism.use_of_uppercase_words(title,content))