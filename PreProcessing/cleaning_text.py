# nltk.download()
import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import TweetTokenizer


class cleaning_text:
    sentence = " Adam"
    tokenized = []
    Pos_tagged = []
    opinion_words = []

    def __init__(self, sentece_input):
        self.sentence = sentece_input

    def tokenizing(self):
        tknzr = TweetTokenizer()
        self.tokenized = tknzr.tokenize(self.sentence)

    def stopword(self):
        filtered = []
        stop_words = set(stopwords.words('english'))
        for w in self.tokenized:
            if w not in stop_words:
                filtered.append(w)
        self.tokenized = filtered
        return self.sentence

    def stemming(self):
        ps = PorterStemmer()
        stemed = []
        for w in self.tokenized:
            word = ps.stem(w)
            stemed.append(word)
        self.tokenized = stemed

    def lower(self):
        self.sentence = self.sentence.lower()
        return self.sentence

    def punctuation(self):
        self.sentence = re.sub('[' + string.punctuation + ']', '', self.sentence)

    def lemmatization(self):
        lemmantizer = WordNetLemmatizer()
        lemma = []
        for w in self.tokenized:
            lemma.append(lemmantizer.lemmatize(w))
        self.tokenized = lemma

    def POS_tagging(self):
        self.Pos_tagged = tagged = nltk.pos_tag(self.tokenized)
