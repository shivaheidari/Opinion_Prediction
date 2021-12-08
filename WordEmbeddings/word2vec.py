import numpy as np
import pandas as pd
from nltk.stem import WordNetLemmatizer


class word2vec:
    df = []
    name = ''

    def __init__(self, name, source_dir, out_dir, model, alternative_words):
        self.name = name
        self.out_dir = out_dir
        self.model = model
        self.source_dir = source_dir
        self.alternative_words = alternative_words

    def get_vector(self, op_tweet, vector):
        vec = 0
        for t in op_tweet:
            if t in self.model.wv.vocab:
                vec = self.model[t]
            else:
                alt_t = self.alternative_words[t]
                if alt_t in self.model.wv.vocab:
                    vec = self.model[alt_t]
                else:
                    print("error: word "+t+" not found")
            vector = np.add(vec.tolist(), vector)
        return vector

    def glove(self):
        des_path = self.out_dir + '/' + self.name + '.json'
        source_path = self.source_dir + '/' + self.name + '.txt'

        df_file = pd.read_json(source_path, orient='records', lines=True)
        df_file.insert(df_file.shape[1], 'vector', [np.zeros(200) for i in range(0, df_file.shape[0])])

        for idx in df_file.index:
            opinion_words = df_file.at[idx, 'opinion_words']
            if len(opinion_words) > 0:
                vector = self.get_vector(opinion_words, df_file.at[idx, 'vector'])
                df_file.at[idx, 'vector'] = vector

        df_file.to_json(des_path, orient='records', lines=True)

        """
        with open('df.json', 'w', encoding='utf-8') as file:
    df.to_json(file, force_ascii=False,, orient='records',lines=True)
    """
