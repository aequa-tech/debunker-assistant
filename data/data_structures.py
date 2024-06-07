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