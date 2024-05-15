from features.nlp.danger_languages.danger_en import Irony_en, Flame_en, Stereotype_en
from features.nlp.danger_languages.danger_it import Irony_it, Flame_it, Stereotype_it






class Irony():
    """
    Class that implements the detection of irony/sarcasm.
    The detection of this pragmatic phenomenon in the texts is obtained thanks to a fine-tuned model starting from Language Models available for Italian.
    """
    def __init__(self):

        self.irony_it = Irony_it()
        self.irony_en = Irony_en()


    def get_irony(self, language, title: str, content: str):

        if language == 'it':
            return self.irony_it.get_irony(title, content)
        elif language == 'en':
            return self.irony_en.get_irony(title, content)
        else:
            return None

class Flame():
    """
    Class that implements the detection of flame.
    The detection of this pragmatic phenomenon in the texts is obtained thanks to a fine-tuned model starting from Language Models available for Italian.
    """
    def __init__(self):

        self.flame_it = Flame_it()
        self.flame_en = Flame_en()


        
    def get_flame(self, language, title: str, content: str):

        if language == 'it':
            return self.flame_it.get_flame(title, content)
        elif language == 'en':
            return self.flame_en.get_flame(title, content)
        else:
            return None

class Stereotype():
    """
    Class that implements the detection of stereotypes.
    The detection of this pragmatic phenomenon in the texts is obtained thanks to a fine-tuned model starting from Language Models available for Italian.
    """
    def __init__(self):

        self.stereotype_it = Stereotype_it()
        self.stereotype_en = Stereotype_en()

        
    def get_stereotype(self, language, title: str, content: str):

        if language == 'it':
            return self.stereotype_it.get_stereotype(title, content)
        elif language == 'en':
            return self.stereotype_en.get_stereotype(title, content)
        else:
            return None

if __name__ == '__main__':

    irony = Irony()
    flame = Flame()
    stereotype = Stereotype()

    apis = {
        "dangerousStyle": {

            'irony': irony.get_irony,
            'flame': flame.get_flame,
            'stereotype': stereotype.get_stereotype,

        },

    }

    for key, value in apis.items():
        for key2, value2 in value.items():
            print(key,key2)
            print(value2("it","titolo di prova","contenuto di prova")["title"]["descriptions"]["absolute"])
            print(value2("en","titolo di prova","contenuto di prova")["title"]["descriptions"]["absolute"])

