# nltk.download()
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class labeling_opinion_words(object):
    def __init__(self, tokens, op_lst,threshold):
        self.op_list = op_lst
        self.tokens = tokens
        self.opinion_words = []
        self.threshold=threshold

    def get_opinion_words(self):
        for w in self.tokens:
            if w in self.op_list:
                self.opinion_words.append(w)

    def get_label(self):
        stance = ''
        sid_obj = SentimentIntensityAnalyzer()
        sentiment_dict = sid_obj.polarity_scores(' '.join(word for word in self.opinion_words))
        label = sentiment_dict['compound']
        discrete_label = 0
        if label > self.threshold:
            discrete_label = 1
        elif label < -self.threshold:
            discrete_label = -1
        else:
            discrete_label = 0
        return label, discrete_label
