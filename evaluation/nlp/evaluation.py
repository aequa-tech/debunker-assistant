import ast
import pandas as pd
from sklearn.feature_selection import SelectKBest, chi2
import numpy as np

class eval_best_fts:
    '''
    this class evaluate the best features for titles or texts, looking at their squared chi computed on labels trusted/untrusted

    PARAMETERS:
    - df : the dataframe containing the features for title and paragraphs
    - k : number of features or examples
    - data: observed data 'title' or 'paragraph'
    - path: path of output file with list of the best features

    OUTPUS:
    - file with list of the best features
    '''
    
    def __init__(self):
        pass

    def select_fts(self, df, data:str) -> list: #attenzione: per affective cambia un po' questo (ragionare su come generalizzarlo)
        columns = []
        for i in df.iloc[1,6].keys():
            if i != 'overall' and i != 'description':
                l= ['_title', '_paragraph']
                if data == "title":
                    columns.append(i+l[1])
                else:
                    columns.append(i+l[0])
        return columns
    
    def get_best_k_fts(self, df, k, path:str, data:str):
        columns= self.select_fts(df, data)
        df = df[columns]
        fs = SelectKBest(chi2, k=k)
        matrix = fs.fit_transform(df, df['labels'].tolist())
        print(fs.get_feature_names_out())
        
        list = fs.get_support()
        # print(list)
        with open(path, "w") as writer:
            for i in range(len(df.columns)):
                print(list(df.columns)[i], list[i], fs.scores_[i])
                writer.write('{} \t {} \t {}\n'.format(list(df.columns)[i], list[i], fs.scores_[i]))

    def get_examples(self, df, k, ft:str, data:str):
        
        row = df.iloc[df[ft].nlargest(k, keep="all").index]
        if data == 'title':
            for i in row[['title', ft, 'label']].values:
                print(i[0], i[1], i[2])
        else:
            for i in row[['paragraph', ft, 'label']].values:
                print(i[0], i[1], i[2])


# class correlation()#Simo: da qui --> da analysis_danger

# class visualization()#Simo: da qui --> da analysis_danger
    
if __name__ == '__main__':

    eval_best_fts = eval_best_fts()
    path='fts_style_titles.tsv'

    file = "./debunker/data/test_set.json"
    
    def titles(self, df):#per i titoli togliere i duplicati
        df_titles = df.drop_duplicates(subset=['title'], keep='last').reset_index()
        return df_titles
    
    def normalize(list):
        return (np.array(list) - np.min(np.array(list)))/(np.max(np.array(list))-np.min(np.array(list)))

#informal style
    def preprocessing_style(file):
        df = pd.DataFrame.from_dict(file)
        df_style = df.loc['informal_style']
        df_style['label'] = ['untrusted' if i == 'blacklist' else 'trusted' for i in df_style['part_of'].tolist()]
        df_style = df_style.dropna()
        df_style = df_style[['_id', 'url', 'title', 'part_of', 'paragraph', 'sensationalism_title', 'sensationalism_paragraph', 'label']] # 'source',
        df_style['sensationalism_paragraph'] = df_style['sensationalism_paragraph'].apply(ast.literal_eval)
        df_style['sensationalism_title'] = df_style['sensationalism_title'].apply(ast.literal_eval)
        df_style['ratio_upper_case_title'] = df_style['sensationalism_title'].apply(lambda x: x['ratio_upper_case']['overall'])
        df_style['ratio_upper_case_paragraph'] = df_style['sensationalism_paragraph'].apply(lambda x: x['ratio_upper_case']['overall'])
        df_style['ratio_vowel_repetition_title'] = df_style['sensationalism_title'].apply(lambda x: x['ratio_vowel_repetition']['overall'])
        df_style['ratio_vowel_repetition_paragraph'] = df_style['sensationalism_paragraph'].apply(lambda x: x['ratio_vowel_repetition']['overall'])
        df_style['punct_count_title'] = df_style['sensationalism_title'].apply(lambda x: x['punct_count']['overall'])
        df_style['punct_count_paragraph'] = df_style['sensationalism_paragraph'].apply(lambda x: x['punct_count']['overall'])
        df_style['check_emoji_title'] = df_style['sensationalism_title'].apply(lambda x: x['check_emoji']['overall'])
        df_style['check_emoji_paragraph'] = df_style['sensationalism_paragraph'].apply(lambda x: x['check_emoji']['overall'])
        df_style['labels'] = ['1' if i == 'untrusted' else '0' for i in df_style['label'].tolist()]

        return df_style

#affective
    def preprocessing_affect(file):
        df = pd.DataFrame.from_dict(file)
        df_aff = df.loc['sentiment_affective']
        df_aff['label'] = ['untrusted' if i == 'blacklist' else 'trusted' for i in df_aff['part_of'].tolist()]
        df_aff = df_aff.dropna()
        df_aff = df_aff[['_id', 'url', 'title', 'part_of', 'paragraph', 'sensationalism_title', 'sensationalism_paragraph', 'label']] # 'source',
        df_aff['sensationalism_paragraph'] = df_aff['sensationalism_paragraph'].apply(ast.literal_eval)
        df_aff['sensationalism_title'] = df_aff['sensationalism_title'].apply(ast.literal_eval)
        
        df_aff['positive_title'] = df_aff['sensationalism_title'].apply(lambda x: x['sentiment_profile']['positive'])
        df_aff['positive_paragraph'] = df_aff['sensationalism_paragraph'].apply(lambda x: x['sentiment_profile']['positive'])
        df_aff['negative_title'] = df_aff['sensationalism_title'].apply(lambda x: x['sentiment_profile']['negative'])
        df_aff['negative_paragraph'] = df_aff['sensationalism_paragraph'].apply(lambda x: x['sentiment_profile']['negative'])
        df_aff['polarity_title'] = df_aff['sensationalism_title'].apply(lambda x: x['sentiment_profile']['polarity'])
        df_aff['polarity_paragraph'] = df_aff['sensationalism_paragraph'].apply(lambda x: x['sentiment_profile']['polarity'])
        df_aff['intensity_title'] = df_aff['sensationalism_title'].apply(lambda x: x['sentiment_profile']['intensity'])
        df_aff['intensity_paragraph'] = df_aff['sensationalism_paragraph'].apply(lambda x: x['sentiment_profile']['intensity'])

        df_aff['anger_title'] = df_aff['sensationalism_title'].apply(lambda x: x['emotion_profile']['anger'])
        df_aff['anger_paragraph'] = df_aff['sensationalism_paragraph'].apply(lambda x: x['emotion_profile']['anger'])
        df_aff['anticipation_title'] = df_aff['sensationalism_title'].apply(lambda x: x['emotion_profile']['anticipation'])
        df_aff['anticipation_paragraph'] = df_aff['sensationalism_paragraph'].apply(lambda x: x['emotion_profile']['anticipation'])
        df_aff['disgust_title'] = df_aff['sensationalism_title'].apply(lambda x: x['emotion_profile']['disgust'])
        df_aff['disgust_paragraph'] = df_aff['sensationalism_paragraph'].apply(lambda x: x['emotion_profile']['disgust'])
        df_aff['fear_title'] = df_aff['sensationalism_title'].apply(lambda x: x['emotion_profile']['fear'])
        df_aff['fear_paragraph'] = df_aff['sensationalism_paragraph'].apply(lambda x: x['emotion_profile']['fear'])
        df_aff['joy_title'] = df_aff['sensationalism_title'].apply(lambda x: x['emotion_profile']['joy'])
        df_aff['joy_paragraph'] = df_aff['sensationalism_paragraph'].apply(lambda x: x['emotion_profile']['joy'])
        df_aff['sadness_title'] = df_aff['sensationalism_title'].apply(lambda x: x['emotion_profile']['sadness'])
        df_aff['sadness_paragraph'] = df_aff['sensationalism_paragraph'].apply(lambda x: x['emotion_profile']['sadness'])
        df_aff['surprice_title'] = df_aff['sensationalism_title'].apply(lambda x: x['emotion_profile']['surprice'])
        df_aff['surprice_paragraph'] = df_aff['sensationalism_paragraph'].apply(lambda x: x['emotion_profile']['surprice'])
        df_aff['trust_title'] = df_aff['sensationalism_title'].apply(lambda x: x['emotion_profile']['trust'])
        df_aff['trust_paragraph'] = df_aff['sensationalism_paragraph'].apply(lambda x: x['emotion_profile']['trust'])
        df_aff['aggressiveness_title'] = df_aff['sensationalism_title'].apply(lambda x: x['emotion_profile']['aggressiveness'])
        df_aff['aggressiveness_paragraph'] = df_aff['sensationalism_paragraph'].apply(lambda x: x['emotion_profile']['aggressiveness'])
        df_aff['contempt_title'] = df_aff['sensationalism_title'].apply(lambda x: x['emotion_profile']['contempt'])
        df_aff['contempt_paragraph'] = df_aff['sensationalism_paragraph'].apply(lambda x: x['emotion_profile']['contempt'])
        df_aff['remorse_title'] = df_aff['sensationalism_title'].apply(lambda x: x['emotion_profile']['remorse'])
        df_aff['remorse_paragraph'] = df_aff['sensationalism_paragraph'].apply(lambda x: x['emotion_profile']['remorse'])
        df_aff['disapproval_title'] = df_aff['sensationalism_title'].apply(lambda x: x['emotion_profile']['disapproval'])
        df_aff['disapproval_paragraph'] = df_aff['sensationalism_paragraph'].apply(lambda x: x['emotion_profile']['disapproval'])
        df_aff['awe_title'] = df_aff['sensationalism_title'].apply(lambda x: x['emotion_profile']['awe'])
        df_aff['awe_paragraph'] = df_aff['sensationalism_paragraph'].apply(lambda x: x['emotion_profile']['awe'])
        df_aff['submission_title'] = df_aff['sensationalism_title'].apply(lambda x: x['emotion_profile']['submission'])
        df_aff['submission_paragraph'] = df_aff['sensationalism_paragraph'].apply(lambda x: x['emotion_profile']['submission'])
        df_aff['love_title'] = df_aff['sensationalism_title'].apply(lambda x: x['emotion_profile']['love'])
        df_aff['love_paragraph'] = df_aff['sensationalism_paragraph'].apply(lambda x: x['emotion_profile']['love'])
        df_aff['optimism_title'] = df_aff['sensationalism_title'].apply(lambda x: x['emotion_profile']['optimism'])
        df_aff['optimism_paragraph'] = df_aff['sensationalism_paragraph'].apply(lambda x: x['emotion_profile']['optimism'])

        df_aff['positve_paragraph'] = normalize(df_aff['positive_paragraph'].tolist())
        df_aff['negative_paragraph'] = normalize(df_aff['negative_paragraph'].tolist())
        df_aff['polarity_paragraph'] = normalize(df_aff['polarity_paragraph'].tolist())
        df_aff['positve_title'] = normalize(df_aff['positive_title'].tolist())
        df_aff['negative_title'] = normalize(df_aff['negative_title'].tolist())
        df_aff['polarity_title'] = normalize(df_aff['polarity_title'].tolist())

        return df_aff


    df = titles(preprocessing_style(file))
    eval_best_fts.get_best_k_fts(df, 'all', path, 'title')
    eval_best_fts.get_examples(df, 10, 'ratio_vowel_repetition_title', 'title')
