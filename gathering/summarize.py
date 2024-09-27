import sumy
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.sum_basic import SumBasicSummarizer
from sumy.summarizers.kl import KLSummarizer
from sumy.summarizers.reduction import ReductionSummarizer


class Ranker():
    def __init__(self, input_text, tokenizer=Tokenizer('italian'), summarizer=TextRankSummarizer(), parser=PlaintextParser):
        tokenizer = Tokenizer('italian')
        self.parser = PlaintextParser.from_string(input_text, tokenizer=tokenizer)
        self.summarizer = summarizer
    
    def rank_sents(self):
        ranked = self.summarizer.rate_sentences(self.parser.document)
        ranked = dict(sorted(ranked.items(),key = lambda item:item[1],reverse=True)[:3])
        
        top_ranked = [{'sentence':sent._text,'score':ranked[sent]} for i,sent in enumerate(ranked)]

        return top_ranked
