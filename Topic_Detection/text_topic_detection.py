import pandas as pd
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
import os


# --------------------***private methods***------------------------
def get_min_df(doc_len):
    if doc_len < 1000:
        return 2
    elif doc_len < 10000:
        return 10
    else:
        return 50


def get_max_df(doc_len):
    if doc_len < 100:
        return 1.0
    else:
        return 0.3


# --------------------***main area***------------------------

class text_topic_detection:
    def __init__(self, source_dir, des_file, user_list):
        self.source_dir = source_dir
        self.des_file = des_file
        self.user_list = user_list

    def get_lda_topics(self):
        processed = 0
        for usr in self.user_list:
            processed += 1
            print(processed)
            user = usr[0]
            source_file = self.source_dir + user + '.txt'
            if not os.path.exists(source_file):
                continue
            tw_data = pd.read_csv(source_file, names=['tweet'], header=None)
            if len(tw_data) > 10:
                tw_data.dropna()
                count_vac = CountVectorizer(max_df=get_max_df(len(tw_data)), min_df=get_min_df(len(tw_data)),
                                            stop_words='english', token_pattern='[a-zA-Z]{3,}')
                doc_term_matrix = count_vac.fit_transform(tw_data['tweet'].values.astype('U'))
                print('len: ' + str(len(tw_data)) + ' shape: ' + str(doc_term_matrix.shape))
                lda = LatentDirichletAllocation(n_components=2)
                lda.fit(doc_term_matrix)
                first_topic = lda.components_[0]
                top_topic_words = first_topic.argsort()[-1000:]
                topics = []
                for i in top_topic_words:
                    topics.append(count_vac.get_feature_names()[i])
                with open(self.des_file, 'a+') as fp:
                    fp.write(user + ": ")
                    fp.write(', '.join(topics))
                    fp.write('\n')
