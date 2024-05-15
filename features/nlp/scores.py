import json
from functools import lru_cache
from features.nlp.scores_languages.scores_en import InformalStyle_en, ClickBait_en, Readability_en
from features.nlp.scores_languages.scores_it import InformalStyle_it, ClickBait_it, Readability_it


class InformalStyle:

    def __init__(self):
        self.informal_style_it=InformalStyle_it()
        self.informal_style_en=InformalStyle_en()


    """It uses a personal style: the first and second person (“I” and “you”) and the active voice"""
    @lru_cache(maxsize=32)
    def use_of_first_and_second_person(self,language: str,title: str, content: str):

        if language == 'it':
            return  self.informal_style_it.use_of_first_and_second_person(title, content)
        elif language == 'en':
            return  self.informal_style_en.use_of_first_and_second_person(title, content)
        else:
            return None


    """One of the characteristics of the informal style is the use of a personal style such us personal subject, personal complement and demonstrative pronouns."""
    @lru_cache(maxsize=32)
    def use_of_personal_style(self,language: str, title: str, content: str):
        if language == 'it':
            return self.informal_style_it.use_of_personal_style(title, content)
        elif language == 'en':
            return self.informal_style_en.use_of_personal_style(title, content)
        else:
            return None

    """Evaluate the use of intensifiers that are commonly used in informal styles"""
    @lru_cache(maxsize=32)
    def use_of_intensifier_score(self,language: str, title: str, content: str):
        if language == 'it':
            return self.informal_style_it.use_of_intensifier_score(title, content)
        elif language == 'en':
            return self.informal_style_en.use_of_intensifier_score(title, content)
        else:
            return None

    """Evaluate the use of shorten forms that are commonly used in informal styles"""
    @lru_cache(maxsize=32)
    def use_of_shorten_form_score(self,language: str, title: str, content: str):
        if language == 'it':
            return self.informal_style_it.use_of_shorten_form_score(title, content)
        elif language == 'en':
            return self.informal_style_en.use_of_shorten_form_score(title, content)
        else:
            return None

    """Evaluate the use of shorten forms that are commonly used in informal styles"""
    @lru_cache(maxsize=32)
    def use_of_modals_score(self,language: str, title: str, content: str):
        if language == 'it':
            return self.informal_style_it.use_of_modals_score(title, content)
        elif language == 'en':
            return self.informal_style_en.use_of_modals_score(title, content)
        else:
            return None

    """Evaluate the use of shorten forms that are commonly used in informal styles"""
    @lru_cache(maxsize=32)
    def use_of_interrogative_score(self,language: str, title: str, content: str):
        if language == 'it':
            return self.informal_style_it.use_of_interrogative_score(title, content)
        elif language == 'en':
            return self.informal_style_en.use_of_interrogative_score(title, content)
        else:
            return None

    """It shouts or use other impolite  behaviors"""
    @lru_cache(maxsize=32)
    def use_of_uppercase_words(self,language: str, title: str, content: str):
        if language == 'it':
            return self.informal_style_it.use_of_uppercase_words(title, content)
        elif language == 'en':
            return self.informal_style_en.use_of_uppercase_words(title, content)
        else:
            return None

    """It evaluate the presence of emphasis with formula such us SVEGLIAAA."""
    @lru_cache(maxsize=32)
    def use_of_repeated_letters(self,language: str, title: str, content: str):
        if language == 'it':
            return self.informal_style_it.use_of_repeated_letters(title, content)
        elif language == 'en':
            return self.informal_style_en.use_of_repeated_letters(title, content)
        else:
            return None

    """In informal writing, multiple exclamation points and question marks are sometimes used to indicate stronger emphasis or emotion."""
    @lru_cache(maxsize=32)
    def use_of_aggressive_punctuation(self,language: str, title: str, content: str):
        if language == 'it':
            return self.informal_style_it.use_of_aggressive_punctuation(title, content)
        elif language == 'en':
            return self.informal_style_en.use_of_aggressive_punctuation(title, content)
        else:
            return None

    """In formal writing, the common punktuation marks are limited. The use of other types of punctiation marks could be a cue of the use of an informal style."""
    @lru_cache(maxsize=32)
    def use_of_uncommon_punctuation(self,language: str, title: str, content: str):
        if language == 'it':
            return self.informal_style_it.use_of_uncommon_punctuation(title, content)
        elif language == 'en':
            return self.informal_style_en.use_of_uncommon_punctuation(title, content)
        else:
            return None

    """Emojis are currently use in informal context."""
    @lru_cache(maxsize=32)
    def use_of_emoji(self,language: str, title: str, content: str):
        if language == 'it':
            return self.informal_style_it.use_of_emoji(title, content)
        elif language == 'en':
            return self.informal_style_en.use_of_emoji(title, content)
        else:
            return None

class Readability:

    def __init__(self):
        self.readability_it=Readability_it()
        self.readability_en=Readability_en()
    """It says how easy something is to read."""
    @lru_cache(maxsize=32)
    def flesch_reading_ease(self,language: str, title: str, content: str):
        if language == 'it':
            return self.readability_it.flesch_reading_ease(title, content)
        elif language == 'en':
            return self.readability_en.flesch_reading_ease(title, content)
        else:
            return None


class ClickBait:
    def __init__(self):

        self.clickbait_it=ClickBait_it()
        self.clickbait_en=ClickBait_en()
    """
    Clickbait typically refers to the practice of writing sensationalized or misleading headlines in order to attract clicks on a piece of content.
    A clickbait title tries to pull people into an article by seeming unbelievable or shocking.
    These titles are rarely informative, and the content behind the clickbait doesn't have to be interesting.
    The quality of the article has no bearing on the attention the title gets.
    """

    """Clickbait headlines often add an element of dishonesty, using enticements that do not accurately reflect the content being delivered."""
    def misleading_headline(self,language: str, title: str, content: str):
        if language == 'it':
            return self.clickbait_it.misleading_headline(title, content)
        elif language == 'en':
            return self.clickbait_en.misleading_headline(title, content)
        else:
            return None


if __name__ == '__main__':
    informalStyle = InformalStyle()
    clickBait = ClickBait()
    readability = Readability()
    #sentiment = Sentiment()
    #emotion = Emotion()
    #irony = Irony()
    #flame = Flame()
    #stereotype = Stereotype()
    # network = Network()

    apis = {
        'informalStyle': {
            'use_of_first_and_second_person': informalStyle.use_of_first_and_second_person,
            'use_of_personal_style': informalStyle.use_of_personal_style,
            'use_of_intensifier_score': informalStyle.use_of_intensifier_score,
            'use_of_shorten_form_score': informalStyle.use_of_shorten_form_score,
            'use_of_modals_score': informalStyle.use_of_modals_score,
            'use_of_interrogative_score': informalStyle.use_of_interrogative_score,
            'use_of_uppercase_words': informalStyle.use_of_uppercase_words,
            'use_of_repeated_letters': informalStyle.use_of_repeated_letters,
            'use_of_aggressive_punctuation': informalStyle.use_of_aggressive_punctuation,
            'use_of_uncommon_punctuation': informalStyle.use_of_uncommon_punctuation,
            'use_of_emoji': informalStyle.use_of_emoji,
        },
        "readability": {
            'flesch_reading_ease': readability.flesch_reading_ease,
        },
        "clickBait": {
            'misleading_headline': clickBait.misleading_headline,
        },
    }

    for key, value in apis.items():
        for key2, value2 in value.items():
            print(key,key2)
            print(value2("it","titolo di prova","contenuto di prova")["title"]["values"]["absolute"])
            print(value2("en","titolo di prova","contenuto di prova")["title"]["values"]["absolute"])