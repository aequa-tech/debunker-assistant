import ast
import json
import scipy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import chi2_contingency
from sklearn.feature_selection import SelectKBest, chi2
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

class eval_best_fts:
    '''
    this class evaluates the best features for titles or texts, looking at their squared chi and correlation index computed respect to labels trusted/untrusted

    PARAMETERS:
    - df : the dataframe containing the features for title and paragraphs
    - k : number of features or examples
    - data: observed data 'title' or 'paragraph'
    - feat: feature to be visualized
    - name: name of the file
    - save: boolean value to save or not the best features

    OUTPUS:
    - file with list of the best features
    - print of the squared chi and correlation values
    '''
    
    def __init__(self):
        pass
    
    def select_fts(self, df, data:str) -> list: 
        columns = []
        for i in df.iloc[1,6].items():                
            if i[0] != 'overall' and i[0] != 'description':
                for k in i[1].keys():
                    if k != 'overall' and k != 'description':
                        l= ['_title', '_paragraph']
                        if data == "title":
                            columns.append(k+l[0])
                        else:
                            columns.append(k+l[1])
        return columns
    
    def best_k_fts(self, df, k, name:str, data:str, save=False):
        columns= self.select_fts(df, data)
        feat = df[columns]
        fs = SelectKBest(chi2, k=k)
        matrix = fs.fit_transform(feat, df['labels'])
        # print(fs.get_feature_names_out())
        
        list_ = fs.get_support()
        path = './fts_'+name+'.tsv'
        if save:
            with open(path, "w") as writer:
                for i in range(len(feat.columns)):
                    writer.write('{} \t {} \t {}\n'.format(feat.columns[i], list_[i], fs.scores_[i]))
        else:
            for i in range(len(feat.columns)):
                print(feat.columns[i], list_[i], fs.scores_[i])
           

    def examples(self, df, k, ft:str, data:str):
        
        row = df.iloc[df[ft].nlargest(k, keep="all").index]
        if data == 'title':
            for i in row[['title', ft, 'label']].values:
                print(i[0], i[1], i[2])
        else:
            for i in row[['paragraph', ft, 'label']].values:
                print(i[0], i[1], i[2])

    def contingency_table(self, var1, var2):
        table = pd.crosstab(var1, var2, margins=False)
        return table

    def correlation(self, df, feat:str):
        var1 = df['label'].astype('str')
        var2 = df[feat].astype('str')
    
        stat, p, dof, expected = chi2_contingency(self.contingency_table(var1, var2), correction=False)
        table= pd.crosstab(var1, var2, margins=True)
        print(table, '\n')
        print('frequenze teoriche attese: ')
        print(expected)
    
        print()
        print('Interpretation of chi-squared value: ')
        prob = 0.95
        critical = scipy.stats.chi2.ppf(prob, dof) #livello di significanza in Percent Point Function (PPF)
        print('probability=%.3f, critical=%.3f, chi_2=%.3f' % (prob, critical, stat))
        if abs(stat) >= critical:
            print('Dependent (reject H0)')
        else:
            print('Independent (fail to reject H0)')
    
        print()
        print('Interpretation of p-value: ')
        alpha = 1.0 - prob #(0.05 reseanoble alpha level 5% ottenuto con il 95% di probabilità)
        print('significance=%.3f, p-value=%.3f' % (alpha, p))
        if p <= alpha:
            print('Dependent (reject H0)')
        else:
            print('Independent (fail to reject H0)')

class visualization:
    '''
    this class visualizes the distribution of the scores for each feature respect to labels trusted/untrusted
    
    PARAMETERS:
    - df : the dataframe containing the features for title and paragraphs
    - feat: feature to be visualized
    - name: title of the plot
    - save: boolean value to save or not the boxplot

    OUTPUS:
    - boxplot
    '''
    
    def __init__(self):
        pass

    def distribution(self, df, feat:str, name:str, save=False):
        list_item = [feat]
        fig, axs = plt.subplots(figsize=(20, 6), nrows=1, ncols=len(list_item), squeeze=False)
        fig.suptitle(name)
        for j, indicator in enumerate(list_item):
            g=sns.boxplot(data=df[list_item +['label']], y=indicator, x='label', hue='label', ax=axs[0, j], palette="Set2")
            axs[0, j].get_legend().remove()
            g.set(xlabel=None)
            g.set(ylabel=None)
            g.set(title=indicator)
            if save:
                plt.savefig('./'+name+'.png')

if __name__ == '__main__':

    eval_best_fts = eval_best_fts()
    visualization = visualization()
    
    file = "./debunker/data/test_set.json"

    dfs = []
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for i in data['results']:
            df = pd.DataFrame.from_dict(i)
            dfs.append(df)
    df_ = pd.concat(dfs)
    df = df_[(df_['part_of'] == 'blacklist') | (df_['part_of'] == 'whitelist')] 
    print(df.shape)
    
    def titles(df):#per i titoli togliere i duplicati
        df_titles = df.drop_duplicates(subset=['title'], keep='last').reset_index()
        return df_titles
    
    def normalize(list):
        return (np.array(list) - np.min(np.array(list)))/(np.max(np.array(list))-np.min(np.array(list)))

    #preprocessing overall
    def preprocessing_overall(data):
        df = pd.DataFrame.from_dict(data)
        df_overall = df.loc['overall']
        df_overall['label'] = ['untrusted' if i == 'blacklist' else 'trusted' for i in df_overall['part_of'].tolist()]
        df_overall = df_overall.dropna()
        lists = []
        lists_ = []
        for f in ['sarcasm', 'irony', 'stereotype', 'flame']:
            for s in ['_title', '_paragraph']:
                lists_.append(f+s)
                for i in ['_0', '_1']:
                    lists.append(f+s+i)              
        
        for list in lists_:
            # print(list)
            labels = []
            scores = []
            for i,v in enumerate(df_overall['_id'].values):
                value = []
                for l in lists:
                    if list in l:
                        # print(l, df_overall[[l]].values[i][0])
                        s = df_overall[[l]].values[i][0]
                        value.append(s)
                    
                m = max(value)
                score = -value[0] if value[0] == m else value[1]
                scores.append(score)
                label = '0' if value[0] == m else '1'
                labels.append(label)
            df_overall[list+'_score'] = normalize(scores)
            df_overall[list+'_label'] = labels
       
        return df_overall
    
    #informal style
    def preprocessing_style(data):
        df = pd.DataFrame.from_dict(data)
        df_style = data.loc['informal_style']
        labels = ['untrusted' if i == 'blacklist' else 'trusted' for i in df_style['part_of'].tolist()]
        df_style['label'] = labels
        df_style = df_style.dropna()
        df_style = df_style[['_id', 'url', 'title', 'part_of', 'paragraph', 'sensationalism_title', 'sensationalism_paragraph', 'label']] # 'source',
        # print(df_style.shape)
        df_style['ratio_upper_case_title'] = df_style['sensationalism_title'].apply(lambda x: x['ratio_upper_case']['overall'])
        df_style['ratio_upper_case_paragraph'] = df_style['sensationalism_paragraph'].apply(lambda x: x['ratio_upper_case']['overall'])
        df_style['ratio_vowel_repetition_title'] = df_style['sensationalism_title'].apply(lambda x: x['ratio_vowel_repetition']['overall'])
        df_style['ratio_vowel_repetition_paragraph'] = df_style['sensationalism_paragraph'].apply(lambda x: x['ratio_vowel_repetition']['overall'])
        df_style['punct_count_title'] = df_style['sensationalism_title'].apply(lambda x: x['punct_count']['overall'])
        df_style['punct_count_paragraph'] = df_style['sensationalism_paragraph'].apply(lambda x: x['punct_count']['overall'])
        df_style['check_emoji_title'] = df_style['sensationalism_title'].apply(lambda x: x['check_emoji']['overall'])
        df_style['check_emoji_paragraph'] = df_style['sensationalism_paragraph'].apply(lambda x: x['check_emoji']['overall'])
        df_style['punct_num_normal_title'] = df_style['sensationalism_title'].apply(lambda x: x['punct_count']['punct_num_normal'])
        df_style['punct_num_normal_paragraph'] = df_style['sensationalism_paragraph'].apply(lambda x: x['punct_count']['punct_num_normal'])
        df_style['punct_num_weird_title'] = df_style['sensationalism_title'].apply(lambda x: x['punct_count']['punct_num_weird'])
        df_style['punct_num_weird_paragraph'] = df_style['sensationalism_paragraph'].apply(lambda x: x['punct_count']['punct_num_weird'])
        df_style['labels'] = ['1' if i == 'untrusted' else '0' for i in df_style['label'].tolist()]
        return df_style

    #affective
    def preprocessing_affect(data):
        df = pd.DataFrame.from_dict(data)
        df_aff = data.loc['sentiment_affective']
        df_aff['label'] = ['untrusted' if i == 'blacklist' else 'trusted' for i in df_aff['part_of'].tolist()]
        df_aff = df_aff.dropna()
        df_aff = df_aff[['_id', 'url', 'title', 'part_of', 'paragraph', 'sensationalism_title', 'sensationalism_paragraph', 'label']] # 'source',
        # df_aff['sensationalism_paragraph'] = df_aff['sensationalism_paragraph'].apply(ast.literal_eval)
        # df_aff['sensationalism_title'] = df_aff['sensationalism_title'].apply(ast.literal_eval)
        
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
        df_aff['labels'] = ['1' if i == 'untrusted' else '0' for i in df_aff['label'].tolist()]

        return df_aff

    # df_ = titles(preprocessing_affect(df))
    # eval_best_fts.best_k_fts(df_, 'all', name='aff', data='title', save=False)
    # eval_best_fts.examples(df_, 1, 'ratio_vowel_repetition_title', 'title')

    df_ = titles(preprocessing_overall(df))
    # visualization.distribution(df_, 'stereotype_title_1', name='stereotype_1',  save=True)
    eval_best_fts.correlation(df_, 'flame_paragraph_label')