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

- acronimi (LOL),
- tachigrafie (nn, qnt),
- abbreviazioni (asp raga),
- scriptio continua (chettelodicoaffa),
- uso delle maiuscole per urlare (SVEGLIA!),
- neocòni giocosi (cuorare),
- ibridismi itanglesi (whatsappare)
- presenza di isolati vocaboli dialettali (daje),
- emoticon (<3).

- svegliaaaaa esclamazione/iperbole
- cretini crasi sarcastiche

- dizionario con definizione?
- sentence embeddings bert
-

"""
import json
from typing import Tuple

import spacy
import hashlib
import random
import sys
import re
from functools import lru_cache

import textstat
import emojis

MAX_SIZE=10*1024*1024 #bytes

class InformalStyle:

    def __init__(self) -> None:
        self.nlp = spacy.load("it_core_news_lg") #['tok2vec', 'morphologizer', 'tagger', 'parser', 'lemmatizer', 'senter', 'attribute_ruler', 'ner']
        self.title_features={}
        self.content_features={}

    @lru_cache(maxsize=32)
    def get_nlp(self,text):
        return self.nlp(text)

    """It uses a personal style: the first and second person (“I” and “you”) and the active voice"""
    @lru_cache(maxsize=32)
    def use_of_first_and_second_person(self, title: str, content: str):
        """
        One of the characteristics of the informal style is the use of a personal style, such as the use of first and second person (“I” and “you”) and the use of active voice (e.g., “I have noticed that...”).
        This function evaluate the presence of that phenomenon.

        @param title: str: string containing the title of a news
        @param content: str: string containing the textual content of a news
        @return: dic: a dictionary containing the personal style feature with the following structure

                {
                    "description": "One of the characteristics of the informal style is the use of a personal style, such as the use of first and second person (\u201cI\u201d and \u201cyou\u201d) and the use of active voice (e.g., \u201cI have noticed that...\u201d).",
                    "title": {
                        "first and second person": {
                            "description": "The numbers of times the first and second persons have been used.",
                            "value": 2
                        },
                        "normalized first and second person": {
                            "description": "the fraction between the number of times the first and second persons have been used and the number of verbs",
                            "value": 1.0
                        }
                    },
                    "content": {
                        "first and second person": {
                            "description": "The numbers of times the first and second persons have been used.",
                            "value": 2
                        },
                        "normalized first and second person": {
                            "description": "the fraction between the number of times the first and second persons have been used and the number of verbs",
                            "value": 0.6666666666666666
                        }
                    }
                }
        """

        result={
            "description" : "One of the characteristics of the informal style is the use of a personal style, such as the use of first and second person (“I” and “you”) and the use of active voice (e.g., “I have noticed that...”)."
        }

        features = {"title" : self.get_nlp(title), "content" : self.get_nlp(content),}

        for key, value in features.items():

            personal_style=0
            not_personal_style=0
            for sent in value.sents:
                for token in sent:
                    if token.pos_ == 'VERB':
                        #Mood = Ind | Number = Sing | Person = 1 | Tense = Pres | VerbForm = Fin
                        if token.morph.get("Person") in [['1'],['2']]:
                            personal_style+=1
                        else:
                            not_personal_style+=1

            ratio = personal_style/(personal_style+not_personal_style) if personal_style+not_personal_style>0 else 0
            result[key]={
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

    """One of the characteristics of the informal style is the use of a personal style such us personal subject, personal complement and demonstrative pronouns."""
    @lru_cache(maxsize=32)
    def use_of_personal_style(self, title: str, content: str):
        """
        One of the characteristics of the informal style is the use of a personal style such us personal subject, personal complement and demonstrative pronouns.
        This function evaluate the presence of that phenomenon.

        @param title: str: string containing the title of a news
        @param content: str: string containing the textual content of a news
        @return: dic: a dictionary containing the personal style feature with the following structure

                {
                    "description": "One of the characteristics of the informal style is the use of a personal style, such as the use of personal subject, personal complement and demonstrative pronouns",
                    "title": {
                        "personal style": {
                            "description": "The numbers of times the first and second persons have been used.",
                            "value": 2
                        },
                        "normalized personal style": {
                            "description": "the fraction between the number of times the use of personal subject, personal complement and demonstrative pronouns have been used and the number of words",
                            "value": 1.0
                        }
                    },
                    "content": {
                        "personal style": {
                            "description": "The numbers of times the first and second persons have been used.",
                            "value": 2
                        },
                        "normalized personal style": {
                            "description": "the fraction between the number of times the first and second persons have been used and the number of verbs",
                            "value": 0.6666666666666666
                        }
                    }
                }
        """

        result={
            "description" : "One of the characteristics of the informal style is the use of a personal style such us personal subject, personal complement and demonstrative pronouns."
        }

        features = {"title" : self.get_nlp(title), "content" : self.get_nlp(content),}

        for key, value in features.items():

            personal_style=0
            not_personal_style=0
            for sent in value.sents:
                for token in sent:

                    # personal score
                    personali_soggetto = ['io', 'tu', 'egli', 'ella', 'noi', 'voi', 'essi', 'lui', 'lei', 'loro',
                                          'esso', 'essa', 'esse']
                    personali_complemento = ['me', 'mi', 'te', 'ti', 'lui', 'sé', 'ciò', 'lei', 'lo', 'gli', 'ne',
                                             'si', 'la', 'le', 'noi', 'ci', 'voi', 'vi', 'essi', 'loro', 'esse',
                                             'li', 'le']
                    pronomi_dimostrativi = ['questo', 'codesto', 'quello', 'questa', 'codesta', 'quella', 'questi',
                                            'codesti', 'quelli', 'queste', 'codeste', 'quelle', 'stesso', 'stessa',
                                            'stessi', 'stesse',
                                            'medesimo', 'medesima', 'medesime', 'medesimi', 'tale', 'tali',
                                            'costui', 'costei', 'costoro', 'colui', 'colei', 'coloro', 'ciò']
                    if token.text.lower() in personali_soggetto + personali_complemento + pronomi_dimostrativi:
                        personal_style += 1
                    else:
                        not_personal_style +=1

            ratio = personal_style/(personal_style+not_personal_style) if personal_style+not_personal_style>0 else 0
            result[key]={
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

    """Evaluate the use of intensifiers that are commonly used in informal styles"""
    @lru_cache(maxsize=32)
    def use_of_intensifier_score(self, title: str, content: str):
        """
        Evaluate the use of intensifiers that are commonly used in informal styles
        This function evaluate the presence of that phenomenon.

        @param title: str: string containing the title of a news
        @param content: str: string containing the textual content of a news
        @return: dic: a dictionary containing the intensifier_score feature with the following structure


        """

        result={
            "description" : "Evaluate the use of intensifiers that are commonly used in informal styles"
        }

        features = {"title" : self.get_nlp(title), "content" : self.get_nlp(content),}

        for key, value in features.items():

            positive=0
            negative=0
            for sent in value.sents:
                for token in sent:

                    if token.pos_ == 'ADJ':
                        if 'Degree' in token.morph.to_dict() and (
                                token.morph.to_dict()['Degree'] == 'Sup' or token.morph.to_dict()['Degree'] == 'Abs'):
                            positive += 1
                        else:
                            negative+=1

            ratio = positive/(positive+negative) if positive+negative>0 else 0
            result[key]={
                                            "personal style":
                                                { "description" : f"The numbers of times an intensifier have been used.",
                                                  "value": positive,
                                                },
                                                "normalized personal style":
                                                { "description" : f"the fraction between the number of times an intensifier have been used and the number of adjectives",
                                                  "value" : ratio
                                                }
                                        }
        return result

    """Evaluate the use of shorten forms that are commonly used in informal styles"""
    @lru_cache(maxsize=32)
    def use_of_shorten_form_score(self, title: str, content: str):
        """
        Evaluate the use of shorten forms that are commonly used in informal styles
        This function evaluate the presence of that phenomenon.

        @param title: str: string containing the title of a news
        @param content: str: string containing the textual content of a news
        @return: dic: a dictionary containing the shorten form score feature with the following structure


        """

        result={
            "description" : "Evaluate the use of shorten forms that are commonly used in informal styles"
        }

        features = {"title" : self.get_nlp(title), "content" : self.get_nlp(content),}

        for key, value in features.items():

            positive=0
            negative=0
            for sent in value.sents:
                for token in sent:

                    # shortened_form_score
                    if token.text.lower() in ['xke', 'xké', 'tadb', 'tat', 'k', 'kk', 'tl;dr', 'thx', 'tvtb', 'tvukdb',
                                              'xoxo', 'tbh', 'scnr', 'rly?', 'rofl', 'plz', 'omg', 'omfg', 'nsfw', 'n8',
                                              'n1', 'noob', 'n00b', 'lol', 'irl', 'imho', 'imo', 'idk', 'Hth', 'Hf',
                                              'gratz', 'gg', 'gl', 'gj', 'gn', 'g2g', 'gig', 'fyi', 'faq', 'f2f', 'eod',
                                              'ez', 'dafuq', 'dafuq', 'wtf', 'cya', 'cbcr', 'btw', 'brb', 'bbl', 'bg',
                                              'asap', 'afaik', 'aka', '2L8', '2g4u', 'ime', 'b4', 'rsvp', 'lmk', 'dob',
                                              'eta', 'fomo', 'diy', 'fwiw', 'hmu', 'icymi', 'tbh', 'tbf']:
                        positive += 1
                    else:
                        negative+=1

            ratio = positive/(positive+negative) if positive+negative>0 else 0
            result[key]={
                                            "personal style":
                                                { "description" : f"The numbers of times a shorten form have been used.",
                                                  "value": positive,
                                                },
                                                "normalized personal style":
                                                { "description" : f"the fraction between the number of times a shorten form have been used and the number of words",
                                                  "value" : ratio
                                                }
                                        }
        return result

    """Evaluate the use of shorten forms that are commonly used in informal styles"""
    @lru_cache(maxsize=32)
    def use_of_modals_score(self, title: str, content: str):
        """
        Evaluate the use of modals that are commonly used in informal styles
        This function evaluate the presence of that phenomenon.

        @param title: str: string containing the title of a news
        @param content: str: string containing the textual content of a news
        @return: dic: a dictionary containing the modal score feature with the following structure


        """

        result={
            "description" : "Evaluate the use of modals that are commonly used in informal styles"
        }

        features = {"title" : self.get_nlp(title), "content" : self.get_nlp(content),}

        for key, value in features.items():

            positive=0
            negative=0
            for sent in value.sents:
                for token in sent:

                    # modal_score
                    if token.pos_ == 'VERB':
                        if token.lemma_ in ['potere', 'volere', 'dovere']:
                            positive += 1
                        else:
                            negative+=1

            ratio = positive/(positive+negative) if positive+negative>0 else 0
            result[key]={
                                            "personal style":
                                                { "description" : f"The numbers of times a modal have been used.",
                                                  "value": positive,
                                                },
                                                "normalized personal style":
                                                { "description" : f"the fraction between the number of times a modal have been used and the number of words",
                                                  "value" : ratio
                                                }
                                        }
        return result

    """Evaluate the use of shorten forms that are commonly used in informal styles"""
    @lru_cache(maxsize=32)
    def use_of_interrogative_score(self, title: str, content: str):
        """
        Evaluate the use of interrogative is less common in formal styles
        This function evaluate the presence of that phenomenon.

        @param title: str: string containing the title of a news
        @param content: str: string containing the textual content of a news
        @return: dic: a dictionary containing the modal score feature with the following structure


        """

        result={
            "description" : "Evaluate the use of interrogatives is less commoon in formal styles"
        }

        features = {"title" : self.get_nlp(title), "content" : self.get_nlp(content),}

        for key, value in features.items():

            positive=0
            negative=0
            for sent in value.sents:
                if '?' in sent.text:
                    positive += 1
                else:
                    negative+=1

            ratio = positive/(positive+negative) if positive+negative>0 else 0
            result[key]={
                                            "personal style":
                                                { "description" : f"The numbers interrogative sentences.",
                                                  "value": positive,
                                                },
                                                "normalized personal style":
                                                { "description" : f"the fraction between the number of interrogative sentence and the sentences",
                                                  "value" : ratio
                                                }
                                        }
        return result

    """It shouts or use other impolite  behaviors"""
    @lru_cache(maxsize=32)
    def use_of_uppercase_words(self, title: str, content: str):
        """
        One of the characteristics of the informal style is the use of capital letters used for shouting and other impolite or argumentative behaviors.
        This function evaluate the presence of that phenomenon.

        @param title: str: string containing the title of a news
        @param content: str: string containing the textual content of a news
        @return: dic: a dictionary containing the uppercase words feature with the following structure

                    {
                        "description": "One of the characteristics of the informal style is the use of capital letters used for shouting and other impolite or argumentative behaviors.",
                        "title": {
                            "uppercase words": {
                                "description": "The numbers of uppercase words.",
                                "value": 0
                            },
                            "normalized uppercase words": {
                                "description": "the fraction between the number of uppercase words and the number of words (the acronyms of organisations have been excluded).",
                                "value": 0.0
                            }
                        },
                        "content": {
                            "uppercase words": {
                                "description": "The numbers of uppercase words.",
                                "value": 1
                            },
                            "normalized uppercase words": {
                                "description": "the fraction between the number of uppercase words and the number of words (the acronyms of organisations have been excluded).",
                                "value": 0.125
                            }
                        }
                    }
        """


        result={
            "description" : "One of the characteristics of the informal style is the use of capital letters used for shouting and other impolite or argumentative behaviors."
        }
        features = {"title" : self.get_nlp(title), "content" : self.get_nlp(content),}

        for key, value in features.items():
            uppercase=0
            not_uppercase=0
            for sent in value.sents:
                for token in sent:
                    if len(token.text)>2:
                        if token.text not in [ent.text for ent in sent.ents]: # It excludes acronyms of organisations.
                            if token.text.isupper():
                                uppercase+=1
                            if token.text[1:].islower(): # it excludes the first char
                                not_uppercase+=1

            ratio = uppercase/(uppercase+not_uppercase) if uppercase+not_uppercase>0 else 0
            result[key]={
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

    """It evaluate the presence of emphasis with formula such us SVEGLIAAA."""
    @lru_cache(maxsize=32)
    def use_of_repeated_letters(self, title: str, content: str):
        """
        The excessive use of vowels could be used for emphasis and for expressing rage.

        @param title: str: string containing the title of a news
        @param content: str: string containing the textual content of a news
        @return: dic: a dictionary containing the repeated letters score feature with the following structure
                    {
                        "description": "The excessive use of vowels could be used for emphasis and for expressing rage.",
                        "title": {
                            "repeated letters score": {
                                "description": "The number of words containing excessive number of vowels.",
                                "value": 8
                            },
                            "normalized repeated letters score": {
                                "description": "The fraction between the number of words containing excessive number of vowels and the total number of words in the text.",
                                "value": 0.0
                            }
                        }
                    }
        """

        result={
            "description" : "The excessive use of vowels could be used for emphasis and for expressing rage."
        }
        features = {"title" : title, "content" : content,}

        for key, value in features.items():

            up_pattern = re.compile('[A-z]{1,}([aA]{3,}|[eE]{3,}|[iI]{3,}|[oO]{3,}|[uU]{3,})')
            all_w_pattern = re.compile('\w+')

            n_upper_words = len(re.findall(up_pattern,value))
            n_words = len(re.findall(all_w_pattern,value))

            ratio = n_upper_words/n_words if n_words>0 else 0

            result[key] = {
                "repeated letters score":
                    {
                        "description": f"The number of words containing excessive number of vowels.",
                        "value": n_words,
                        },
                "normalized repeated letters score":
                    {
                        "description": f"The fraction between the number of words containing excessive number of vowels and the total number of words in the text.",
                        "value": ratio
                        }
            }
            return result

    """In informal writing, multiple exclamation points and question marks are sometimes used to indicate stronger emphasis or emotion."""
    @lru_cache(maxsize=32)
    def use_of_aggressive_punctuation(self, title: str, content: str):
        """

        In informal writing, multiple exclamation points and question marks are sometimes used to indicate stronger emphasis or emotion.


        @param title: str: string containing the title of a news
        @param content: str: string containing the textual content of a news
        @return: dic: a dictionary containing the aggressive punctuation score feature with the following structure
                {
                    "description": "In informal writing, multiple exclamation points and question marks are sometimes used to indicate stronger emphasis or emotion.",
                    "title": {
                        "repeated aggressive punctuation": {
                            "description": "The number of multiple exclamation points and/or question marks.",
                            "value": 1
                        },
                        "normalized repeated letters score": {
                            "description": "The fraction between the number of multiple exclamation points and/or question marks and the total number of exclamation points and question marks.",
                            "value": 0.125
                        }
                    }
                }
        """
        result = {
            "description":     "In informal writing, multiple exclamation points and question marks are sometimes used to indicate stronger emphasis or emotion."
        }
        features = {"title": title, "content": content, }

        for key, value in features.items():
            up_pattern = re.compile('[!?]{2,}')
            all_w_pattern = re.compile('[!?]{1}')

            presence_phenomenon = len(re.findall(up_pattern, value))
            n_words = len(re.findall(all_w_pattern, value))

            ratio = presence_phenomenon / n_words if n_words > 0 else 0

            result[key] = {
                "repeated aggressive punctuation":
                    {
                        "description": f"The number of multiple exclamation points and/or question marks.",
                        "value": presence_phenomenon,
                    },
                "normalized repeated letters score":
                    {
                        "description": f"The fraction between the number of multiple exclamation points and/or question marks and the total number of exclamation points and question marks.",
                        "value": ratio
                    }
            }
            return result

    """In formal writing, the common punktuation marks are limited. The use of other types of punctiation marks could be a cue of the use of an informal style."""
    @lru_cache(maxsize=32)
    def use_of_uncommon_punctuation(self, title: str, content: str):
        """

        In formal writing, the common punktuation marks are limited. The use of other types of punctiation marks could be a cue of the use of an informal style.

        @param title: str: string containing the title of a news
        @param content: str: string containing the textual content of a news
        @return: dic: a dictionary containing the uncommon punctuation score feature with the following structure

                    {
                        "description": "In informal writing, multiple exclamation points and question marks are sometimes used to indicate stronger emphasis or emotion.",
                        "title": {
                            "uncommon punctiation score": {
                                "description": "The number of uncommon punctuation marks.",
                                "value": 5
                            },
                            "normalized uncommon punctiation score": {
                                "description": "The fraction between the number of uncommon punctuation marks and the total number of punctuation marks.",
                                "value": 0.5555555555555556
                            }
                        }
                    }
        """
        result = {
            "description":     "In informal writing, multiple exclamation points and question marks are sometimes used to indicate stronger emphasis or emotion."
        }
        features = {"title": title, "content": content, }

        for key, value in features.items():

            punct_normal = re.compile('(\?|\.|\,|\;|\:)')
            punct_weird = re.compile('(\!|(\.\.\.)|…|\*|\=|\$)')

            presence_phenomenon = len(re.findall(punct_weird, value))
            negative_phenomenon = len(re.findall(punct_normal, value))

            ratio = presence_phenomenon / (negative_phenomenon+presence_phenomenon) if negative_phenomenon > 0 else 0

            result[key] = {
                "uncommon punctiation score":
                    {
                        "description": f"The number of uncommon punctuation marks.",
                        "value": presence_phenomenon,
                    },
                "normalized uncommon punctiation score":
                    {
                        "description": f"The fraction between the number of uncommon punctuation marks and the total number of punctuation marks.",
                        "value": ratio
                    }
            }
            return result

    """Emojis are currently use in informal context."""
    @lru_cache(maxsize=32)
    def use_of_emoji(self, title: str, content: str):
        """

        Emojis are currently use in informal contexts.

        @param title: str: string containing the title of a news
        @param content: str: string containing the textual content of a news
        @return: dic: a dictionary containing the emoji score feature with the following structure

                {
                    "description": "Emojis are currently use in informal contexts.",
                    "title": {
                        "repeated aggressive punctuation": {
                            "description": "The number of uncommon punctuation marks.",
                            "value": 0
                        },
                        "normalized repeated letters score": {
                            "description": "The fraction between the number of uncommon punctuation marks and the total number of punctuation marks.",
                            "value": 0.0
                        }
                    }
                }

        """
        result = {
            "description":     "Emojis are currently use in informal contexts."
        }
        features = {"title": title, "content": content, }

        for key, value in features.items():
            print(emojis.get(value))
            presence_phenomenon = len(emojis.get(value))
            all_w_pattern = re.compile('\w+')
            n_words = len(re.findall(all_w_pattern,value))
            ratio = presence_phenomenon / n_words if n_words > 0 else 0

            result[key] = {
                "repeated aggressive punctuation":
                    {
                        "description": f"The number of emojis.",
                        "value": presence_phenomenon,
                    },
                "normalized repeated letters score":
                    {
                        "description": f"The fraction between the number of emojis and the total number tokens in the text.",
                        "value": ratio
                    }
            }
            return result











    """It says how easy something is to read."""
    @lru_cache(maxsize=32)
    def readability_score(self, title: str, content: str):
        """
        The readability score is computes with the Flesch Reading Ease (FRES) score. It says how easy something is to read.
        This function evaluate the presence of that phenomenon.

        @param title: str: string containing the title of a news
        @param content: str: string containing the textual content of a news
        @return: dic: a dictionary containing the readability score feature with the following structure

                    {
                        "description": "The readability score is computes with the Flesch Reading Ease (FRES) score. It says how easy something is to read.",
                        "title": {
                            "readability_scores": {
                                "description": "The Flesch Reading Ease (FRES) score. The maximum score is 121.22, there is no limit on how low the score can be. A negative score is valid. 90-100\tVery Easy, 60-69 Standard, 0-29\tVery Confusing.",
                                "value": 114.12
                            },
                            "normalized readability_scores": {
                                "description": "The normalized Flesch Reading Ease (FRES) score. 1 is a standard value, 0 is far from a standard value.",
                                "value": 1
                            }
                        },
                        "content": {
                            "readability score": {
                                "description": "The Flesch Reading Ease (FRES) score. The maximum score is 121.22, there is no limit on how low the score can be. A negative score is valid. 90-100\tVery Easy, 60-69 Standard, 0-29\tVery Confusing.",
                                "value": 68.77
                            },
                            "normalized readability score": {
                                "description": "The normalized Flesch Reading Ease (FRES) score. 1 is a standard value, 0 is far from a standard value.",
                                "value": 1
                            }
                        }
                    }

        """
        result={
            "description" : "The readability score is computes with the Flesch Reading Ease (FRES) score. It says how easy something is to read."
        }
        features = {"title" : title, "content" : content,}

        for key, value in features.items():
            flesch_reading_ease = textstat.flesch_reading_ease(value)
            #the maximum score is 121.22, there is no limit on how low the score can be. A negative score is valid.
            #90-100	Very Easy
            #60-69	Standard
            #0-29	Very Confusing
            if flesch_reading_ease >= 60 and  flesch_reading_ease <= 69:
                normalized_flesch_reading_ease=1
            elif flesch_reading_ease>69:
                normalized_flesch_reading_ease=flesch_reading_ease-69/121.22-69
            elif flesch_reading_ease > 0 and  flesch_reading_ease < 69:
                normalized_flesch_reading_ease = flesch_reading_ease - 0 / 60 - 0
            else:
                normalized_flesch_reading_ease = 0

            if normalized_flesch_reading_ease > 1:
                normalized_flesch_reading_ease = 1
            elif normalized_flesch_reading_ease<0:
                normalized_flesch_reading_ease = 0

            normalized_flesch_reading_ease=abs(normalized_flesch_reading_ease-1)
            result[key]={
                                            "readability score":
                                                { "description" : f"The Flesch Reading Ease (FRES) score. The maximum score is 121.22, there is no limit on how low the score can be. A negative score is valid. 90-100	Very Easy, 60-69 Standard, 0-29	Very Confusing.",
                                                  "value": flesch_reading_ease,
                                                },
                                                "normalized readability score":
                                                { "description" : f"The normalized Flesch Reading Ease (FRES) score. 0 is a standard value, 1 is far from a standard value.",
                                                  "value" : normalized_flesch_reading_ease
                                                }
                                        }
        return result



if __name__ == '__main__':
    scores = InformalStyle()


    title='Io sto! bene tu stai! male NBC, CNN!?!??!'
    content='Io sto bene tu stai male lui è stato picchiato CAZZOOO'
    import time

    # Start timer
    start_time = time.perf_counter()

    #for i in range(0,10000):
    print(json.dumps(scores.use_of_interrogative_score(title, content), indent=4))
    print(json.dumps(scores.use_of_personal_style(title, content), indent=4))
    print(json.dumps(scores.use_of_modals_score(title, content), indent=4))
    print(json.dumps(scores.use_of_emoji(title, content), indent=4))
    print(json.dumps(scores.use_of_interrogative_score(title, content), indent=4))
    print(json.dumps(scores.use_of_intensifier_score(title, content), indent=4))
    print(json.dumps(scores.use_of_aggressive_punctuation(title, content), indent=4))
    print(json.dumps(scores.use_of_shorten_form_score(title, content), indent=4))
    print(json.dumps(scores.use_of_uncommon_punctuation(title, content), indent=4))
    print(json.dumps(scores.use_of_uppercase_words(title, content), indent=4))
    print(json.dumps(scores.use_of_repeated_letters(title, content), indent=4))
    print(json.dumps(scores.use_of_first_and_second_person(title, content), indent=4))
    # End timer
    end_time = time.perf_counter()

    # Calculate elapsed time
    elapsed_time = end_time - start_time
    print("Elapsed time: ", elapsed_time)
    #Elapsed time:  0.15938275000000002
