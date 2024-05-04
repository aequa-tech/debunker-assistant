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

#maxsize=32 number of elements that can be stored in the cache


personali_soggetto = {"it": ['io', 'tu', 'egli', 'ella', 'noi', 'voi', 'essi', 'lui', 'lei', 'loro', 'esso', 'essa', 'esse'],
                      "en": ['io', 'tu', 'egli', 'ella', 'noi', 'voi', 'essi', 'lui', 'lei', 'loro', 'esso', 'essa', 'esse'],

                      }
personali_complemento = {"it": ['me', 'mi', 'te', 'ti', 'lui', 'sé', 'ciò', 'lei', 'lo', 'gli', 'ne',
                                 'si', 'la', 'le', 'noi', 'ci', 'voi', 'vi', 'essi', 'loro', 'esse',
                                 'li', 'le'],
                         "en": ['me', 'mi', 'te', 'ti', 'lui', 'sé', 'ciò', 'lei', 'lo', 'gli', 'ne',
                                 'si', 'la', 'le', 'noi', 'ci', 'voi', 'vi', 'essi', 'loro', 'esse',
                                 'li', 'le']
                         }
pronomi_dimostrativi = {"it":['questo', 'codesto', 'quello', 'questa', 'codesta', 'quella', 'questi',
                                'codesti', 'quelli', 'queste', 'codeste', 'quelle', 'stesso', 'stessa',
                                'stessi', 'stesse',
                                'medesimo', 'medesima', 'medesime', 'medesimi', 'tale', 'tali',
                                'costui', 'costei', 'costoro', 'colui', 'colei', 'coloro', 'ciò'],
                        "en":['questo', 'codesto', 'quello', 'questa', 'codesta', 'quella', 'questi',
                                'codesti', 'quelli', 'queste', 'codeste', 'quelle', 'stesso', 'stessa',
                                'stessi', 'stesse',
                                'medesimo', 'medesima', 'medesime', 'medesimi', 'tale', 'tali',
                                'costui', 'costei', 'costoro', 'colui', 'colei', 'coloro', 'ciò'],
                        }


class MyNlp:
    def __init__(self) -> None:
        self.nlp={}
        self.nlp["it"]= spacy.load("it_core_news_lg")
        self.nlp["en"]= spacy.load("en_core_web_lg")
        self.title_features = {}
        self.content_features = {}

    @lru_cache(maxsize=32)
    def get_nlp(self, language,text):
        return self.nlp[language](text)

nlp=MyNlp()

class InformalStyle:

    """It uses a personal style: the first and second person (“I” and “you”) and the active voice"""
    @lru_cache(maxsize=32)
    def use_of_first_and_second_person(self, language:str,title: str, content: str):
        """
        One of the characteristics of the informal style is the use of a personal style, such as the use of first and second person (“I” and “you”) and the use of active voice (e.g., “I have noticed that...”).
        This function evaluate the presence of that phenomenon.

        @param title: str: string containing the title of a news
        @param content: str: string containing the textual content of a news
        @return: dic: a dictionary containing the personal style feature with the following structure

                        {
                                 "description" :
                                         {
                                                "en": "english description.",
                                                "it": "descrizione in italiano"
                                         },
                                "title": {
                                    "values": {

                                        "absolute": absolute,
                                        "local_normalisation": normalisation,
                                        "global_normalisation": None,
                                    },
                                    "descriptions": {

                                                "absolute": {
                                                    "en": "english description.",
                                                    "it": "descrizione in italiano"
                                                },
                                               "local_normalisation":
                                                {
                                                    "en": "english description of the used normalisation method.",
                                                    "it": "descrizione in italiano del metodo di normalizzazione adottato"
                                                },
                                               "global_normalisation":
                                                {
                                                    "en": "english description of the used global normalisation method.",
                                                    "it": "descrizione in italiano del metodo di normalizzazione globale adottato"
                                                }
                                        }
                                    }
                            "content": {
                                    "values": {

                                                "absolute": absolute,
                                                "local_normalisation": normalisation,
                                                "global_normalisation": None,
                                    },
                                    "descriptions":
                                               {
                                                    "absolute": {
                                                        "en": "english description.",
                                                        "it": "descrizione in italiano"
                                                    },
                                                   "local_normalisation":
                                                    {
                                                        "en": "english description of the used normalisation method.",
                                                        "it": "descrizione in italiano del metodo di normalizzazione adottato"
                                                    },
                                                   "global_normalisation":
                                                    {
                                                        "en": "english description of the used global normalisation method.",
                                                        "it": "descrizione in italiano del metodo di normalizzazione globale adottato"
                                                    }
                                                }
                                    }
                        }
        """
        result={
            "description":
                {
                    "en": "One of the characteristics of the informal style is the use of a personal style, such as the use of first and second person (“I” and “you”) and the use of active voice (e.g., “I have noticed that...”).",
                    "it": "descrizione in italiano"
                },
        }

        features = {"title" : nlp.get_nlp(language,title), "content" : nlp.get_nlp(language,content),}

        for key, value in features.items():

            absolute_positive=0
            absolute_negative=0
            for sent in value.sents:
                for token in sent:
                    if token.pos_ == 'VERB':
                        #Mood = Ind | Number = Sing | Person = 1 | Tense = Pres | VerbForm = Fin
                        if token.morph.get("Person") in [['1'],['2']]:
                            absolute_positive+=1
                        else:
                            absolute_negative+=1

            normalisation_local = absolute_positive/(absolute_positive+absolute_negative) if absolute_positive+absolute_negative>0 else 0
            result[key]  =  {
                                "values": {

                                            "absolute": absolute_positive,
                                            "local_normalisation": normalisation_local,
                                            "global_normalisation": None,
                                },
                                "descriptions": {

                                            "absolute": {
                                                "en": "The numbers of times the first and second persons have been used.",
                                                "it": "Il numero di volte che prima e seconda persona verbale sono usate"
                                            },
                                           "local_normalisation":
                                            {   "en": "the fraction between the number of times the first and second persons have been used and the number of verbs",
                                                "it": "Il rapporto tra il numero di volte sono state usate le forme in prima e seconda persona, rispetto al numero di verbi"
                                            },
                                           "global_normalisation":
                                            {   "en": None,
                                                "it": None
                                            }
                                    }
                            }




        return result


    """One of the characteristics of the informal style is the use of a personal style such us personal subject, personal complement and demonstrative pronouns."""
    @lru_cache(maxsize=32)
    def use_of_personal_style(self, language:str,title: str, content: str):
        """
        One of the characteristics of the informal style is the use of a personal style such us personal subject, personal complement and demonstrative pronouns.
        This function evaluate the presence of that phenomenon.

        @param title: str: string containing the title of a news
        @param content: str: string containing the textual content of a news
        @return: dic: a dictionary containing the personal style feature with the following structure

                        {
                             "description" :
                                     {
                                            "en": "english description.",
                                            "it": "descrizione in italiano"
                                     },
                            "title": {
                                    "values": {

                                        "absolute": absolute,
                                        "local_normalisation": normalisation,
                                        "global_normalisation": None,
                                    },
                                    "descriptions": {

                                                "absolute": {
                                                    "en": "english description.",
                                                    "it": "descrizione in italiano"
                                                },
                                               "local_normalisation":
                                                {
                                                    "en": "english description of the used normalisation method.",
                                                    "it": "descrizione in italiano del metodo di normalizzazione adottato"
                                                },
                                               "global_normalisation":
                                                {
                                                    "en": "english description of the used global normalisation method.",
                                                    "it": "descrizione in italiano del metodo di normalizzazione globale adottato"
                                                }
                                        }
                                    }
                            "content": {
                                    "values": {

                                                "absolute": absolute,
                                                "local_normalisation": normalisation,
                                                "global_normalisation": None,
                                    },
                                    "descriptions":
                                               {
                                                    "absolute": {
                                                        "en": "english description.",
                                                        "it": "descrizione in italiano"
                                                    },
                                                   "local_normalisation":
                                                    {
                                                        "en": "english description of the used normalisation method.",
                                                        "it": "descrizione in italiano del metodo di normalizzazione adottato"
                                                    },
                                                   "global_normalisation":
                                                    {
                                                        "en": "english description of the used global normalisation method.",
                                                        "it": "descrizione in italiano del metodo di normalizzazione globale adottato"
                                                    }
                                                }
                                    }
                        }

        """

        result={
            "description":
                {
                    "en": "One of the characteristics of the informal style is the use of a personal style such us personal subject, personal complement and demonstrative pronouns.",
                    "it": "descrizione in italiano"
                },
        }
        features = {"title" : nlp.get_nlp(language,title), "content" : nlp.get_nlp(language,content),}

        for key, value in features.items():

            absolute_positive=0
            absolute_negative=0
            for sent in value.sents:
                for token in sent:

                    # personal score
                    current_personali_soggetto =  personali_soggetto[language]
                    current_personali_complemento = personali_complemento[language]
                    current_pronomi_dimostrativi = pronomi_dimostrativi[language]

                    if token.text.lower() in current_personali_soggetto + current_personali_complemento + current_pronomi_dimostrativi:
                        absolute_positive += 1
                    else:
                        absolute_negative +=1

            normalisation_local = absolute_positive/(absolute_positive+absolute_negative) if absolute_positive+absolute_negative>0 else 0

            result[key] = {
                                "values": {

                                    "absolute": absolute_positive,
                                    "local_normalisation": normalisation_local,
                                    "global_normalisation": None,
                                },
                                "descriptions": {

                                    "absolute": {
                                        "en": "The number of times a personal style such us personal subject, personal complement or demonstrative pronouns has been used.",
                                        "it": "Il numero di volte che un soggetto personale, complemento personale o pronome dimostrativo è stato utilizzato"
                                    },
                                    "local_normalisation":
                                        {
                                            "en": "the fraction between the number of times personal style have been used and the number of words",
                                            "it": "Il rapporto tra il numero di volte lo stile personale è stato usato, rispetto al numero di parole"
                                            },
                                    "global_normalisation":
                                        {"en": None,
                                         "it": None
                                         }
                                }
                            }

        return result

    """Evaluate the use of intensifiers that are commonly used in informal styles"""
    @lru_cache(maxsize=32)
    def use_of_intensifier_score(self, language:str,title: str, content: str):
        """
        Evaluate the use of intensifiers that are commonly used in informal styles
        This function evaluate the presence of that phenomenon.

        @param title: str: string containing the title of a news
        @param content: str: string containing the textual content of a news
        @return: dic: a dictionary containing the intensifier_score feature with the following structure

                        {
                                     "description" :
                                             {
                                                    "en": "english description.",
                                                    "it": "descrizione in italiano"
                                             },
                                    "title": {
                                    "values": {

                                        "absolute": absolute,
                                        "local_normalisation": normalisation,
                                        "global_normalisation": None,
                                    },
                                    "descriptions": {

                                                "absolute": {
                                                    "en": "english description.",
                                                    "it": "descrizione in italiano"
                                                },
                                               "local_normalisation":
                                                {
                                                    "en": "english description of the used normalisation method.",
                                                    "it": "descrizione in italiano del metodo di normalizzazione adottato"
                                                },
                                               "global_normalisation":
                                                {
                                                    "en": "english description of the used global normalisation method.",
                                                    "it": "descrizione in italiano del metodo di normalizzazione globale adottato"
                                                }
                                        }
                                    }
                            "content": {
                                    "values": {

                                                "absolute": absolute,
                                                "local_normalisation": normalisation,
                                                "global_normalisation": None,
                                    },
                                    "descriptions":
                                               {
                                                    "absolute": {
                                                        "en": "english description.",
                                                        "it": "descrizione in italiano"
                                                    },
                                                   "local_normalisation":
                                                    {
                                                        "en": "english description of the used normalisation method.",
                                                        "it": "descrizione in italiano del metodo di normalizzazione adottato"
                                                    },
                                                   "global_normalisation":
                                                    {
                                                        "en": "english description of the used global normalisation method.",
                                                        "it": "descrizione in italiano del metodo di normalizzazione globale adottato"
                                                    }
                                                }
                                    }
                        }


        """


        result={
            "description":
                {
                    "en": "Evaluate the use of intensifiers that are commonly used in informal styles",
                    "it": "descrizione in italiano"
                },
        }
        features = {"title" : nlp.get_nlp(language,title), "content" : nlp.get_nlp(language,content),}

        for key, value in features.items():

            absolute_positive=0
            absolute_negative=0
            for sent in value.sents:
                for token in sent:

                    if token.pos_ == 'ADJ':
                        if 'Degree' in token.morph.to_dict() and (
                                token.morph.to_dict()['Degree'] == 'Sup' or token.morph.to_dict()['Degree'] == 'Abs'):
                            absolute_positive += 1
                        else:
                            absolute_negative+=1

            normalisation_local = absolute_positive/(absolute_positive+absolute_negative) if absolute_positive+absolute_negative>0 else 0
            result[key] = {
                "values": {

                    "absolute": absolute_positive,
                    "local_normalisation": normalisation_local,
                    "global_normalisation": None,
                },
                "descriptions": {

                    "absolute": {
                        "en": "One of the characteristics of the informal style is the use of a personal style such us personal subject, personal complement and demonstrative pronouns.",
                        "it": "Il numero di volte che prima e seconda persona verbale sono usate"
                    },
                    "local_normalisation":
                        {
                            "en": "the fraction between the number of times the first and second persons have been used and the number of verbs",
                            "it": "Il rapporto tra il numero di volte sono state usate le forme in prima e seconda persona, rispetto al numero di verbi"
                        },
                    "global_normalisation":
                        {"en": None,
                         "it": None
                         }
                }
            }

        return result

    """Evaluate the use of shorten forms that are commonly used in informal styles"""
    @lru_cache(maxsize=32)
    def use_of_shorten_form_score(self, language:str,title: str, content: str):
        """
        Evaluate the use of shorten forms that are commonly used in informal styles
        This function evaluate the presence of that phenomenon.

        @param title: str: string containing the title of a news
        @param content: str: string containing the textual content of a news
        @return: dic: a dictionary containing the shorten form score feature with the following structure

                        {
                                     "description" :
                                             {
                                                    "en": "english description.",
                                                    "it": "descrizione in italiano"
                                             },                            "title": {
                                    "values": {

                                        "absolute": absolute,
                                        "local_normalisation": normalisation,
                                        "global_normalisation": None,
                                    },
                                    "descriptions": {

                                                "absolute": {
                                                    "en": "english description.",
                                                    "it": "descrizione in italiano"
                                                },
                                               "local_normalisation":
                                                {
                                                    "en": "english description of the used normalisation method.",
                                                    "it": "descrizione in italiano del metodo di normalizzazione adottato"
                                                },
                                               "global_normalisation":
                                                {
                                                    "en": "english description of the used global normalisation method.",
                                                    "it": "descrizione in italiano del metodo di normalizzazione globale adottato"
                                                }
                                        }
                                    }
                            "content": {
                                    "values": {

                                                "absolute": absolute,
                                                "local_normalisation": normalisation,
                                                "global_normalisation": None,
                                    },
                                    "descriptions":
                                               {
                                                    "absolute": {
                                                        "en": "english description.",
                                                        "it": "descrizione in italiano"
                                                    },
                                                   "local_normalisation":
                                                    {
                                                        "en": "english description of the used normalisation method.",
                                                        "it": "descrizione in italiano del metodo di normalizzazione adottato"
                                                    },
                                                   "global_normalisation":
                                                    {
                                                        "en": "english description of the used global normalisation method.",
                                                        "it": "descrizione in italiano del metodo di normalizzazione globale adottato"
                                                    }
                                                }
                                    }
                        }

        """


        result={
            "description":
                {
                    "en": "Evaluate the use of shorten forms that are commonly used in informal styles",
                    "it": "descrizione in italiano"
                },
        }
        features = {"title" : nlp.get_nlp(language,title), "content" : nlp.get_nlp(language,content),}

        for key, value in features.items():

            absolute_positive=0
            absolute_negative=0
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
                        absolute_positive += 1
                    else:
                        absolute_negative+=1


            normalisation_local = absolute_positive/(absolute_positive+absolute_negative) if absolute_positive+absolute_negative>0 else 0
            result[key] = {
                                "values": {

                                    "absolute": absolute_positive,
                                    "local_normalisation": normalisation_local,
                                    "global_normalisation": None,
                                },
                                "descriptions": {

                                    "absolute": {
                                        "en": "The numbers of times a shorten form have been used.",
                                        "it": "Il numero di volte che è stata utilizzata una forma abbreviata"
                                    },
                                    "local_normalisation":
                                        {
                                            "en": "The fraction between the number of times a shorten form have been used and the number of words",
                                            "it": "Il rapporto tra il numero di volte una forma abbreviata è stata usata, rispetto al numero di parole"
                                            },
                                    "global_normalisation":
                                        {"en": None,
                                         "it": None
                                         }
                                }
                            }

        return result

    """Evaluate the use of shorten forms that are commonly used in informal styles"""
    @lru_cache(maxsize=32)
    def use_of_modals_score(self, language:str,title: str, content: str):
        """
        Evaluate the use of modals that are commonly used in informal styles
        This function evaluate the presence of that phenomenon.

        @param title: str: string containing the title of a news
        @param content: str: string containing the textual content of a news
        @return: dic: a dictionary containing the modal score feature with the following structure

                        {
                                     "description" :
                                             {
                                                    "en": "english description.",
                                                    "it": "descrizione in italiano"
                                             },                            "title": {
                                    "values": {

                                        "absolute": absolute,
                                        "local_normalisation": normalisation,
                                        "global_normalisation": None,
                                    },
                                    "descriptions": {

                                                "absolute": {
                                                    "en": "english description.",
                                                    "it": "descrizione in italiano"
                                                },
                                               "local_normalisation":
                                                {
                                                    "en": "english description of the used normalisation method.",
                                                    "it": "descrizione in italiano del metodo di normalizzazione adottato"
                                                },
                                               "global_normalisation":
                                                {
                                                    "en": "english description of the used global normalisation method.",
                                                    "it": "descrizione in italiano del metodo di normalizzazione globale adottato"
                                                }
                                        }
                                    }
                            "content": {
                                    "values": {

                                                "absolute": absolute,
                                                "local_normalisation": normalisation,
                                                "global_normalisation": None,
                                    },
                                    "descriptions":
                                               {
                                                    "absolute": {
                                                        "en": "english description.",
                                                        "it": "descrizione in italiano"
                                                    },
                                                   "local_normalisation":
                                                    {
                                                        "en": "english description of the used normalisation method.",
                                                        "it": "descrizione in italiano del metodo di normalizzazione adottato"
                                                    },
                                                   "global_normalisation":
                                                    {
                                                        "en": "english description of the used global normalisation method.",
                                                        "it": "descrizione in italiano del metodo di normalizzazione globale adottato"
                                                    }
                                                }
                                    }
                        }

        """

        result={
            "description":
                {
                    "en": "Evaluate the use of modals that are commonly used in informal styles",
                    "it": "descrizione in italiano"
                },
        }
        features = {"title" : nlp.get_nlp(language,title), "content" : nlp.get_nlp(language,content),}

        for key, value in features.items():

            absolute_positive=0
            absolute_negative=0
            for sent in value.sents:
                for token in sent:

                    # modal_score
                    if token.pos_ == 'VERB':
                        if token.lemma_ in ['potere', 'volere', 'dovere']:
                            absolute_positive += 1
                        else:
                            absolute_negative+=1

            normalisation_local = absolute_positive/(absolute_positive+absolute_negative) if absolute_positive+absolute_negative>0 else 0


            result[key] = {
                                "values": {

                                    "absolute": absolute_positive,
                                    "local_normalisation": normalisation_local,
                                    "global_normalisation": None,
                                },
                                "descriptions": {

                                    "absolute": {
                                        "en": "The numbers of times a modal have been used.",
                                        "it": "Il numero di volte che è stato usato un verbo modale"
                                    },
                                    "local_normalisation":
                                        {
                                            "en": "the fraction between the number of times a modal have been used and the number of verbs",
                                            "it": "Il rapporto tra il numero di volte che è stato usato un verbo modale, rispetto al numero di verbi"
                                            },
                                    "global_normalisation":
                                        {"en": None,
                                         "it": None
                                         }
                                }
                            }

        return result

    """Evaluate the use of shorten forms that are commonly used in informal styles"""
    @lru_cache(maxsize=32)
    def use_of_interrogative_score(self, language:str,title: str, content: str):
        """
        Evaluate the use of interrogative is less common in formal styles
        This function evaluate the presence of that phenomenon.

        @param title: str: string containing the title of a news
        @param content: str: string containing the textual content of a news
        @return: dic: a dictionary containing the modal score feature with the following structure

                        {
                                     "description" :
                                             {
                                                    "en": "english description.",
                                                    "it": "descrizione in italiano"
                                             },                            "title": {
                                    "values": {

                                        "absolute": absolute,
                                        "local_normalisation": normalisation,
                                        "global_normalisation": None,
                                    },
                                    "descriptions": {

                                                "absolute": {
                                                    "en": "english description.",
                                                    "it": "descrizione in italiano"
                                                },
                                               "local_normalisation":
                                                {
                                                    "en": "english description of the used normalisation method.",
                                                    "it": "descrizione in italiano del metodo di normalizzazione adottato"
                                                },
                                               "global_normalisation":
                                                {
                                                    "en": "english description of the used global normalisation method.",
                                                    "it": "descrizione in italiano del metodo di normalizzazione globale adottato"
                                                }
                                        }
                                    }
                            "content": {
                                    "values": {

                                                "absolute": absolute,
                                                "local_normalisation": normalisation,
                                                "global_normalisation": None,
                                    },
                                    "descriptions":
                                               {
                                                    "absolute": {
                                                        "en": "english description.",
                                                        "it": "descrizione in italiano"
                                                    },
                                                   "local_normalisation":
                                                    {
                                                        "en": "english description of the used normalisation method.",
                                                        "it": "descrizione in italiano del metodo di normalizzazione adottato"
                                                    },
                                                   "global_normalisation":
                                                    {
                                                        "en": "english description of the used global normalisation method.",
                                                        "it": "descrizione in italiano del metodo di normalizzazione globale adottato"
                                                    }
                                                }
                                    }
                        }
        """


        result={
            "description":
                {
                    "en": "Evaluate the use of interrogatives is less commoon in formal styles",
                    "it": "descrizione in italiano"
                },
        }
        features = {"title" : nlp.get_nlp(language,title), "content" : nlp.get_nlp(language,content),}

        for key, value in features.items():

            absolute_positive=0
            absolute_negative=0
            for sent in value.sents:
                if '?' in sent.text:
                    absolute_positive += 1
                else:
                    absolute_negative+=1

            normalisation_local = absolute_positive/(absolute_positive+absolute_negative) if absolute_positive+absolute_negative>0 else 0

            result[key] = {
                                "values": {

                                    "absolute": absolute_positive,
                                    "local_normalisation": normalisation_local,
                                    "global_normalisation": None,
                                },
                                "descriptions": {

                                    "absolute": {
                                        "en": "The numbers interrogative sentences.",
                                        "it": "Il numero di frasi interrogative"
                                    },
                                    "local_normalisation":
                                        {
                                            "en": "the fraction between the number of interrogative sentence and the sentences",
                                            "it": "La frazione tra il numero di frasi negative ed il numero totale di frasi"
                                            },
                                    "global_normalisation":
                                        {"en": None,
                                         "it": None
                                         }
                                }
                            }

        return result

    """It shouts or use other impolite  behaviors"""
    @lru_cache(maxsize=32)
    def use_of_uppercase_words(self, language:str,title: str, content: str):
        """
        One of the characteristics of the informal style is the use of capital letters used for shouting and other impolite or argumentative behaviors.
        This function evaluate the presence of that phenomenon.

        @param title: str: string containing the title of a news
        @param content: str: string containing the textual content of a news
        @return: dic: a dictionary containing the uppercase words feature with the following structure

                        {
                                     "description" :
                                             {
                                                    "en": "english description.",
                                                    "it": "descrizione in italiano"
                                             },                            "title": {
                                    "values": {

                                        "absolute": absolute,
                                        "local_normalisation": normalisation,
                                        "global_normalisation": None,
                                    },
                                    "descriptions": {

                                                "absolute": {
                                                    "en": "english description.",
                                                    "it": "descrizione in italiano"
                                                },
                                               "local_normalisation":
                                                {
                                                    "en": "english description of the used normalisation method.",
                                                    "it": "descrizione in italiano del metodo di normalizzazione adottato"
                                                },
                                               "global_normalisation":
                                                {
                                                    "en": "english description of the used global normalisation method.",
                                                    "it": "descrizione in italiano del metodo di normalizzazione globale adottato"
                                                }
                                        }
                                    }
                            "content": {
                                    "values": {

                                                "absolute": absolute,
                                                "local_normalisation": normalisation,
                                                "global_normalisation": None,
                                    },
                                    "descriptions":
                                               {
                                                    "absolute": {
                                                        "en": "english description.",
                                                        "it": "descrizione in italiano"
                                                    },
                                                   "local_normalisation":
                                                    {
                                                        "en": "english description of the used normalisation method.",
                                                        "it": "descrizione in italiano del metodo di normalizzazione adottato"
                                                    },
                                                   "global_normalisation":
                                                    {
                                                        "en": "english description of the used global normalisation method.",
                                                        "it": "descrizione in italiano del metodo di normalizzazione globale adottato"
                                                    }
                                                }
                                    }
                        }

        """



        result={
            "description":
                {
                    "en": "One of the characteristics of the informal style is the use of capital letters used for shouting and other impolite or argumentative behaviors.",
                    "it": "descrizione in italiano"
                },
        }
        features = {"title" : nlp.get_nlp(language,title), "content" : nlp.get_nlp(language,content),}

        for key, value in features.items():
            absolute_positive=0
            absolute_negative=0
            for sent in value.sents:
                for token in sent:
                    if len(token.text)>2:
                        if token.text not in [ent.text for ent in sent.ents]: # It excludes acronyms of organisations.
                            if token.text.isupper():
                                absolute_positive+=1
                            if token.text[1:].islower(): # it excludes the first char
                                absolute_negative+=1

            normalisation_local = absolute_positive/(absolute_positive+absolute_negative) if absolute_positive+absolute_negative>0 else 0

            result[key] = {
                                "values": {

                                    "absolute": absolute_positive,
                                    "local_normalisation": normalisation_local,
                                    "global_normalisation": None,
                                },
                                "descriptions": {

                                    "absolute": {
                                        "en": "The numbers of uppercase words (the acronyms of organisations have been excluded).",
                                        "it": "Il numero di parole totalmente in maiuscolo (gli acronimi delle organizzazioni non sono riconosciuti)"
                                    },
                                    "local_normalisation":
                                        {
                                            "en": "the fraction between the number of uppercase words and the number of words (the acronyms of organisations have been excluded).",
                                            "it": "la frazione tra il numero di parole maiuscole e il numero di parole (sono stati esclusi gli acronimi delle organizzazioni)."
                                            },
                                    "global_normalisation":
                                        {"en": None,
                                         "it": None
                                         }
                                }
                            }

        return result

    """It evaluate the presence of emphasis with formula such us SVEGLIAAA."""
    @lru_cache(maxsize=32)
    def use_of_repeated_letters(self, language:str,title: str, content: str):
        """
        The excessive use of vowels could be used for emphasis and for expressing rage.

        @param title: str: string containing the title of a news
        @param content: str: string containing the textual content of a news
        @return: dic: a dictionary containing the repeated letters score feature with the following structure

                        {
                                     "description" :
                                             {
                                                    "en": "english description.",
                                                    "it": "descrizione in italiano"
                                             },                            "title": {
                                    "values": {

                                        "absolute": absolute,
                                        "local_normalisation": normalisation,
                                        "global_normalisation": None,
                                    },
                                    "descriptions": {

                                                "absolute": {
                                                    "en": "english description.",
                                                    "it": "descrizione in italiano"
                                                },
                                               "local_normalisation":
                                                {
                                                    "en": "english description of the used normalisation method.",
                                                    "it": "descrizione in italiano del metodo di normalizzazione adottato"
                                                },
                                               "global_normalisation":
                                                {
                                                    "en": "english description of the used global normalisation method.",
                                                    "it": "descrizione in italiano del metodo di normalizzazione globale adottato"
                                                }
                                        }
                                    }
                            "content": {
                                    "values": {

                                                "absolute": absolute,
                                                "local_normalisation": normalisation,
                                                "global_normalisation": None,
                                    },
                                    "descriptions":
                                               {
                                                    "absolute": {
                                                        "en": "english description.",
                                                        "it": "descrizione in italiano"
                                                    },
                                                   "local_normalisation":
                                                    {
                                                        "en": "english description of the used normalisation method.",
                                                        "it": "descrizione in italiano del metodo di normalizzazione adottato"
                                                    },
                                                   "global_normalisation":
                                                    {
                                                        "en": "english description of the used global normalisation method.",
                                                        "it": "descrizione in italiano del metodo di normalizzazione globale adottato"
                                                    }
                                                }
                                    }
                        }

        """


        result={
            "description":
                {
                    "en": "The excessive use of vowels could be used for emphasis and for expressing rage.",
                    "it": "descrizione in italiano"
                },
        }
        features = {"title" : title, "content" : content,}

        for key, value in features.items():

            pattern_positive = re.compile('[A-z]{1,}([aA]{3,}|[eE]{3,}|[iI]{3,}|[oO]{3,}|[uU]{3,})')
            pattern_negative = re.compile('\w+')

            absolute_positive = len(re.findall(pattern_positive,value))
            absolute_total = len(re.findall(pattern_negative,value))

            normalisation_local = absolute_positive/absolute_total if absolute_total>0 else 0


            result[key] = {
                                "values": {

                                    "absolute": absolute_positive,
                                    "local_normalisation": normalisation_local,
                                    "global_normalisation": None,
                                },
                                "descriptions": {

                                    "absolute": {
                                        "en": "The number of words containing excessive number of vowels.",
                                        "it": "Il numero di parole che contengono un numero ecessivo di vocali"
                                    },
                                    "local_normalisation":
                                        {
                                            "en": "The fraction between the number of words containing excessive number of vowels and the total number of words in the text.",
                                            "it": "Il rapporto tra il numero di parole che contengono un numero ecessivo di vocali e il numero totale di vocali"
                                            },
                                    "global_normalisation":
                                        {"en": None,
                                         "it": None
                                         }
                                }
                            }

        return result

    """In informal writing, multiple exclamation points and question marks are sometimes used to indicate stronger emphasis or emotion."""
    @lru_cache(maxsize=32)
    def use_of_aggressive_punctuation(self, language:str,title: str, content: str):
        """

        In informal writing, multiple exclamation points and question marks are sometimes used to indicate stronger emphasis or emotion.


        @param title: str: string containing the title of a news
        @param content: str: string containing the textual content of a news
        @return: dic: a dictionary containing the aggressive punctuation score feature with the following structure

                        {
                                     "description" :
                                             {
                                                    "en": "english description.",
                                                    "it": "descrizione in italiano"
                                             },                            "title": {
                                    "values": {

                                        "absolute": absolute,
                                        "local_normalisation": normalisation,
                                        "global_normalisation": None,
                                    },
                                    "descriptions": {

                                                "absolute": {
                                                    "en": "english description.",
                                                    "it": "descrizione in italiano"
                                                },
                                               "local_normalisation":
                                                {
                                                    "en": "english description of the used normalisation method.",
                                                    "it": "descrizione in italiano del metodo di normalizzazione adottato"
                                                },
                                               "global_normalisation":
                                                {
                                                    "en": "english description of the used global normalisation method.",
                                                    "it": "descrizione in italiano del metodo di normalizzazione globale adottato"
                                                }
                                        }
                                    }
                            "content": {
                                    "values": {

                                                "absolute": absolute,
                                                "local_normalisation": normalisation,
                                                "global_normalisation": None,
                                    },
                                    "descriptions":
                                               {
                                                    "absolute": {
                                                        "en": "english description.",
                                                        "it": "descrizione in italiano"
                                                    },
                                                   "local_normalisation":
                                                    {
                                                        "en": "english description of the used normalisation method.",
                                                        "it": "descrizione in italiano del metodo di normalizzazione adottato"
                                                    },
                                                   "global_normalisation":
                                                    {
                                                        "en": "english description of the used global normalisation method.",
                                                        "it": "descrizione in italiano del metodo di normalizzazione globale adottato"
                                                    }
                                                }
                                    }
                        }

        """


        result={
            "description":
                {
                    "en": "In informal writing, multiple exclamation points and question marks are sometimes used to indicate stronger emphasis or emotion.",
                    "it": "descrizione in italiano"
                },
        }
        features = {"title": title, "content": content, }

        for key, value in features.items():
            pattern_positive = re.compile('[!?]{2,}')
            pattern_total = re.compile('[!?]{1}')

            absolute_positive = len(re.findall(pattern_positive, value))
            absolute_total = len(re.findall(pattern_total, value))

            normalisation_local = absolute_positive / absolute_total if absolute_total > 0 else 0

            result[key] = {
                                "values": {

                                    "absolute": absolute_positive,
                                    "local_normalisation": normalisation_local,
                                    "global_normalisation": None,
                                },
                                "descriptions": {

                                    "absolute": {
                                        "en": "The number of multiple exclamation points and/or question marks.",
                                        "it": "Il numero di più punti esclamativi e/o interrogativi."
                                    },
                                    "local_normalisation":
                                        {
                                            "en": "The fraction between the number of multiple exclamation points and/or question marks and the total number of exclamation points and question marks.",
                                            "it": "La frazione tra il numero di più punti esclamativi e/o interrogativi e il numero totale di punti esclamativi e punti interrogativi."
                                            },
                                    "global_normalisation":
                                        {"en": None,
                                         "it": None
                                         }
                                }
                            }

        return result

    """In formal writing, the common punktuation marks are limited. The use of other types of punctiation marks could be a cue of the use of an informal style."""
    @lru_cache(maxsize=32)
    def use_of_uncommon_punctuation(self, language:str,title: str, content: str):
        """

        In formal writing, the common punktuation marks are limited. The use of other types of punctiation marks could be a cue of the use of an informal style.

        @param title: str: string containing the title of a news
        @param content: str: string containing the textual content of a news
        @return: dic: a dictionary containing the uncommon punctuation score feature with the following structure


                        {
                                     "description" :
                                             {
                                                    "en": "english description.",
                                                    "it": "descrizione in italiano"
                                             },                            "title": {
                                    "values": {

                                        "absolute": absolute,
                                        "local_normalisation": normalisation,
                                        "global_normalisation": None,
                                    },
                                    "descriptions": {

                                                "absolute": {
                                                    "en": "english description.",
                                                    "it": "descrizione in italiano"
                                                },
                                               "local_normalisation":
                                                {
                                                    "en": "english description of the used normalisation method.",
                                                    "it": "descrizione in italiano del metodo di normalizzazione adottato"
                                                },
                                               "global_normalisation":
                                                {
                                                    "en": "english description of the used global normalisation method.",
                                                    "it": "descrizione in italiano del metodo di normalizzazione globale adottato"
                                                }
                                        }
                                    }
                            "content": {
                                    "values": {

                                                "absolute": absolute,
                                                "local_normalisation": normalisation,
                                                "global_normalisation": None,
                                    },
                                    "descriptions":
                                               {
                                                    "absolute": {
                                                        "en": "english description.",
                                                        "it": "descrizione in italiano"
                                                    },
                                                   "local_normalisation":
                                                    {
                                                        "en": "english description of the used normalisation method.",
                                                        "it": "descrizione in italiano del metodo di normalizzazione adottato"
                                                    },
                                                   "global_normalisation":
                                                    {
                                                        "en": "english description of the used global normalisation method.",
                                                        "it": "descrizione in italiano del metodo di normalizzazione globale adottato"
                                                    }
                                                }
                                    }
                        }

        """

        result={
            "description":
                {
                    "en": "In informal writing, multiple exclamation points and question marks are sometimes used to indicate stronger emphasis or emotion.",
                    "it": "descrizione in italiano"
                },
        }
        features = {"title": title, "content": content, }

        for key, value in features.items():

            absolute_negative = re.compile('(\?|\.|\,|\;|\:)')
            absolute_positive = re.compile('(\!|(\.\.\.)|…|\*|\=|\$)')

            absolute_positive = len(re.findall(absolute_positive, value))
            absolute_negative = len(re.findall(absolute_negative, value))

            normalisation_local = absolute_positive / (absolute_negative+absolute_positive) if absolute_negative > 0 else 0


            result[key] = {
                                "values": {

                                    "absolute": absolute_positive,
                                    "local_normalisation": normalisation_local,
                                    "global_normalisation": None,
                                },
                                "descriptions": {

                                    "absolute": {
                                        "en": "The number of uncommon punctuation marks.",
                                        "it": "Il numero di segni di punteggiatura non comuni."
                                    },
                                    "local_normalisation":
                                        {
                                            "en": "The fraction between the number of uncommon punctuation marks and the total number of punctuation marks.",
                                            "it": "La frazione tra il numero di segni di punteggiatura non comuni e il numero totale di segni di punteggiatura."
                                            },
                                    "global_normalisation":
                                        {"en": None,
                                         "it": None
                                         }
                                }
                            }

        return result

    """Emojis are currently use in informal context."""
    @lru_cache(maxsize=32)
    def use_of_emoji(self, language:str,title: str, content: str):
        """

        Emojis are currently use in informal contexts.

        @param title: str: string containing the title of a news
        @param content: str: string containing the textual content of a news
        @return: dic: a dictionary containing the emoji score feature with the following structure


                        {
                                     "description" :
                                             {
                                                    "en": "english description.",
                                                    "it": "descrizione in italiano"
                                             },                            "title": {
                                    "values": {

                                        "absolute": absolute,
                                        "local_normalisation": normalisation,
                                        "global_normalisation": None,
                                    },
                                    "descriptions": {

                                                "absolute": {
                                                    "en": "english description.",
                                                    "it": "descrizione in italiano"
                                                },
                                               "local_normalisation":
                                                {
                                                    "en": "english description of the used normalisation method.",
                                                    "it": "descrizione in italiano del metodo di normalizzazione adottato"
                                                },
                                               "global_normalisation":
                                                {
                                                    "en": "english description of the used global normalisation method.",
                                                    "it": "descrizione in italiano del metodo di normalizzazione globale adottato"
                                                }
                                        }
                                    }
                            "content": {
                                    "values": {

                                                "absolute": absolute,
                                                "local_normalisation": normalisation,
                                                "global_normalisation": None,
                                    },
                                    "descriptions":
                                               {
                                                    "absolute": {
                                                        "en": "english description.",
                                                        "it": "descrizione in italiano"
                                                    },
                                                   "local_normalisation":
                                                    {
                                                        "en": "english description of the used normalisation method.",
                                                        "it": "descrizione in italiano del metodo di normalizzazione adottato"
                                                    },
                                                   "global_normalisation":
                                                    {
                                                        "en": "english description of the used global normalisation method.",
                                                        "it": "descrizione in italiano del metodo di normalizzazione globale adottato"
                                                    }
                                                }
                                    }
                        }


        """

        result={
            "description":
                {
                    "en": "Emojis are currently use in informal contexts.",
                    "it": "descrizione in italiano"
                },
        }
        features = {"title": title, "content": content, }

        for key, value in features.items():
            absolute_positive = len(emojis.get(value))
            pattern_total = re.compile('\w+')
            absolute_negative = len(re.findall(pattern_total,value))
            normalisation_local = absolute_positive / absolute_negative if absolute_negative > 0 else 0


            result[key] = {
                                "values": {

                                    "absolute": absolute_positive,
                                    "local_normalisation": normalisation_local,
                                    "global_normalisation": None,
                                },
                                "descriptions": {

                                    "absolute": {
                                        "en": "The number of emojis.",
                                        "it": "Il numero di emoji"
                                    },
                                    "local_normalisation":
                                        {
                                            "en": "The fraction between the number of emojis and the total number tokens in the text.",
                                            "it": "Il rapporto tra il numero di emoji e il numero di tokens nel testo"
                                            },
                                    "global_normalisation":
                                        {"en": None,
                                         "it": None
                                         }
                                }
                            }

        return result

class Readability:
    """It says how easy something is to read."""
    @lru_cache(maxsize=32)
    def flesch_reading_ease(self, language:str,title: str, content: str):
        """
        The readability score is computes with the Flesch Reading Ease (FRES) score. It says how easy something is to read.
        This function evaluate the presence of that phenomenon.

        @param title: str: string containing the title of a news
        @param content: str: string containing the textual content of a news
        @return: dic: a dictionary containing the readability score feature with the following structure


                        {
                                     "description" :
                                             {
                                                    "en": "english description.",
                                                    "it": "descrizione in italiano"
                                             },
                                    "title": {
                                    "values": {

                                        "absolute": absolute,
                                        "local_normalisation": normalisation,
                                        "global_normalisation": None,
                                    },
                                    "descriptions": {

                                                "absolute": {
                                                    "en": "english description.",
                                                    "it": "descrizione in italiano"
                                                },
                                               "local_normalisation":
                                                {
                                                    "en": "english description of the used normalisation method.",
                                                    "it": "descrizione in italiano del metodo di normalizzazione adottato"
                                                },
                                               "global_normalisation":
                                                {
                                                    "en": "english description of the used global normalisation method.",
                                                    "it": "descrizione in italiano del metodo di normalizzazione globale adottato"
                                                }
                                        }
                                    }
                            "content": {
                                    "values": {

                                                "absolute": absolute,
                                                "local_normalisation": normalisation,
                                                "global_normalisation": None,
                                    },
                                    "descriptions":
                                               {
                                                    "absolute": {
                                                        "en": "english description.",
                                                        "it": "descrizione in italiano"
                                                    },
                                                   "local_normalisation":
                                                    {
                                                        "en": "english description of the used normalisation method.",
                                                        "it": "descrizione in italiano del metodo di normalizzazione adottato"
                                                    },
                                                   "global_normalisation":
                                                    {
                                                        "en": "english description of the used global normalisation method.",
                                                        "it": "descrizione in italiano del metodo di normalizzazione globale adottato"
                                                    }
                                                }
                                    }
                        }


        """

        result={
            "description":
                {
                    "en": "The readability score is computes with the Flesch Reading Ease (FRES) score. It says how easy something is to read.",
                    "it": "descrizione in italiano"
                },
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
                normalized_flesch_reading_ease = (flesch_reading_ease - 0) / (60 - 0)
            else:
                normalized_flesch_reading_ease = 0

            if normalized_flesch_reading_ease > 1:
                normalized_flesch_reading_ease = 1
            elif normalized_flesch_reading_ease<0:
                normalized_flesch_reading_ease = 0

            normalized_flesch_reading_ease=abs(normalized_flesch_reading_ease-1)


            result[key] = {
                                "values": {

                                    "absolute": flesch_reading_ease,
                                    "local_normalisation": normalized_flesch_reading_ease,
                                    "global_normalisation": None,
                                },
                                "descriptions": {

                                    "absolute": {
                                        "en": "The Flesch Reading Ease (FRES) score. The maximum score is 121.22, there is no limit on how low the score can be. A negative score is valid. 90-100	Very Easy, 60-69 Standard, 0-29	Very Confusing.",
                                        "it": "Il punteggio Flesch Reading Ease (FRES). Il punteggio massimo è 121,22, non c'è limite a quanto basso possa essere il punteggio. Un punteggio negativo è valido. 90-100 Molto facile, 60-69 Standard, 0-29 Molto confuso."
                                    },
                                    "local_normalisation":
                                        {
                                            "en": "The normalized Flesch Reading Ease (FRES) score. 0 is a standard value, 1 is far from a standard value.",
                                            "it": "Il punteggio Flesch Reading Ease (FRES) normalizzato. 0 è un valore standard, 1 è lontano da un valore standard."
                                            },
                                    "global_normalisation":
                                        {"en": None,
                                         "it": None
                                         }
                                }

                        }
        return result

class ClickBait:
    """
    Clickbait typically refers to the practice of writing sensationalized or misleading headlines in order to attract clicks on a piece of content.
    A clickbait title tries to pull people into an article by seeming unbelievable or shocking.
    These titles are rarely informative, and the content behind the clickbait doesn't have to be interesting.
    The quality of the article has no bearing on the attention the title gets.
    """

    """Clickbait headlines often add an element of dishonesty, using enticements that do not accurately reflect the content being delivered."""
    def misleading_headline(self, language:str, title: str, content: str):
        """
        Clickbait headlines often add an element of dishonesty, using enticements that do not accurately reflect the content being delivered.

        @param title: str: string containing the title of a news
        @param content: str: string containing the textual content of a news
        @return: dic: a dictionary containing the misleading_headline feature with the following structure

                        {
                            "description" :
                                             {
                                                    "en": "english description.",
                                                    "it": "descrizione in italiano"
                                             },
                            "title": {
                                    "values": {

                                        "absolute": absolute,
                                        "local_normalisation": normalisation,
                                        "global_normalisation": None,
                                    },
                                    "descriptions": {

                                                "absolute": {
                                                    "en": "english description.",
                                                    "it": "descrizione in italiano"
                                                },
                                               "local_normalisation":
                                                {
                                                    "en": "english description of the used normalisation method.",
                                                    "it": "descrizione in italiano del metodo di normalizzazione adottato"
                                                },
                                               "global_normalisation":
                                                {
                                                    "en": "english description of the used global normalisation method.",
                                                    "it": "descrizione in italiano del metodo di normalizzazione globale adottato"
                                                }
                                        }
                                    }
                            "content": {
                                    "values": {

                                                "absolute": absolute,
                                                "local_normalisation": normalisation,
                                                "global_normalisation": None,
                                    },
                                    "descriptions":
                                               {
                                                    "absolute": {
                                                        "en": "english description.",
                                                        "it": "descrizione in italiano"
                                                    },
                                                   "local_normalisation":
                                                    {
                                                        "en": "english description of the used normalisation method.",
                                                        "it": "descrizione in italiano del metodo di normalizzazione adottato"
                                                    },
                                                   "global_normalisation":
                                                    {
                                                        "en": "english description of the used global normalisation method.",
                                                        "it": "descrizione in italiano del metodo di normalizzazione globale adottato"
                                                    }
                                                }
                                    }
                        }

        """

        result={
            "description":
                {
                    "en": "Clickbait headlines often add an element of dishonesty, using enticements that do not accurately reflect the content being delivered.",
                    "it": "descrizione in italiano"
                },
        }
        title_nouns = nlp.get_nlp(language,' '.join([str(t) for t in nlp.get_nlp(language,title) if t.pos_ in ['VERB','NOUN', 'PROPN']]))
        content_nouns = nlp.get_nlp(language,' '.join([str(t) for t in nlp.get_nlp(language,content) if t.pos_ in ['VERB','NOUN', 'PROPN']]))

        doc_similarity=title_nouns.similarity(content_nouns)

        features = {"title" : title, "content" : content,}

        for key, value in features.items():
            result[key] = {
                "values": {

                    "absolute": doc_similarity,
                    "local_normalisation": abs(1-doc_similarity),
                    "global_normalisation": None,
                },
                "descriptions": {

                    "absolute": {
                        "en": "The similarity between the title and the content in the range 0 (completely different) and 1 (the same text).",
                        "it": "La somiglianza tra il titolo e il contenuto è compresa tra 0 (completamente diverso) e 1 (lo stesso testo)."
                    },
                    "local_normalisation":
                        {
                            "en": "The normalized similarity between the title and the content in the range 0 (the same text) and 1 (completely different).",
                            "it": "La somiglianza normalizzata tra il titolo e il contenuto nell'intervallo 0 (lo stesso testo) e 1 (completamente diverso)."
                        },
                    "global_normalisation":
                        {"en": None,
                         "it": None
                         }
                }

            }

        return result



if __name__ == '__main__':
    scores = InformalStyle()
    scores2 = ClickBait()
    scores3 = Readability()


    title='Io sto! bene tu stai! male NBC, CNN!?!??!'
    content='questa è una frase molto comprensibile'
    import time

    # Start timer
    start_time = time.perf_counter()

    #for i in range(0,10000):
    print(json.dumps(scores2.misleading_headline("it",title, content), indent=4))


    print(json.dumps(scores.use_of_first_and_second_person("it",title, content), indent=4))
    print(json.dumps(scores.use_of_interrogative_score("en",title, content), indent=4))
    print(json.dumps(scores.use_of_personal_style("en",title, content), indent=4))
    print(json.dumps(scores.use_of_modals_score("en",title, content), indent=4))
    print(json.dumps(scores.use_of_emoji("en",title, content), indent=4))
    print(json.dumps(scores.use_of_interrogative_score("en",title, content), indent=4))
    print(json.dumps(scores.use_of_intensifier_score("en",title, content), indent=4))
    print(json.dumps(scores.use_of_aggressive_punctuation("en",title, content), indent=4))
    print(json.dumps(scores.use_of_shorten_form_score("en",title, content), indent=4))
    print(json.dumps(scores.use_of_uncommon_punctuation("it",title, content), indent=4))
    print(json.dumps(scores.use_of_uppercase_words("it",title, content), indent=4))
    print(json.dumps(scores.use_of_repeated_letters("it",title, content), indent=4))
    print(json.dumps(scores3.flesch_reading_ease("it",title, content), indent=4))
    # End timer
    end_time = time.perf_counter()

    # Calculate elapsed time
    elapsed_time = end_time - start_time
    print("Elapsed time: ", elapsed_time)
    #Elapsed time:  0.15938275000000002
