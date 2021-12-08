# label each tweet of each user using labeling algorithms
# visualization of changes according to time
import codecs
import json
import os
import pycld2 as cld2
# nltk.download()
import pandas as pd
from nltk.corpus import opinion_lexicon
from cleaning_text import cleaning_text
from labeling_opinion_words import labeling_opinion_words
# from ..Utils import Utils
""" ---------------------private method area----------------------------------------"""

def language_detect(tweet_text):
    lang = "non"
    try:
        isReliable, textBytesFound, details = cld2.detect(tweet_text)
        if details[0][2] > 50:
            lang = details[0][1]
    except:
        lang = "non"
    return lang


def set_output_directory():
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)


def get_file_path(u_name):
    # user might be on of main users or on of main users friends
    if os.path.exists(users_source_dir + '/' + u_name + '.txt'):
        return users_source_dir + '/' + u_name + '.txt'

    if os.path.exists(friends_source_dir + '/' + u_name + '.txt'):
             return friends_source_dir + '/' + u_name + '.txt'
    return ""


def process_user_tweets(des, u_name):
    en_tweets = 0
    json_tweets = []

    s_file = get_file_path(u_name)
    if s_file=="":
        print(u_name+".txt not found")
        return
    df_file = pd.read_json(codecs.open(s_file, 'r', 'utf-8'), orient='records', lines=True)

    """ batch_clean_text : remove urls and  charachters and numbers
     it make language detections more accurate"""
    url_regex = r'(\S+[.]){2,}[^\s]+|\S+:\/\/(\S+[.])+[^\s]+'
    df_file['tweet'] = df_file['tweet'].str.replace(url_regex, '', case=False)
    # filtering the entire dataset for only english
    df_file['Language'] = df_file['tweet'].apply(lambda x: language_detect(x))
    df_file = df_file.drop(df_file.loc[df_file['Language'] != 'en'].index)

    for idx in df_file.index:
        l = 0
        dl = 0
        tweet_text = df_file.at[idx, 'tweet']
        en_tweets = en_tweets + 1
        pre_obj = cleaning_text(tweet_text)
        pre_obj.lower()
        pre_obj.punctuation()
        pre_obj.tokenizing()
        pre_obj.stopword()
        pre_obj.stemming()

        tokens = getattr(pre_obj, 'tokenized')
        labeling_opinions = labeling_opinion_words(tokens, op_lst, threshold)
        labeling_opinions.get_opinion_words()

        if len(labeling_opinions.opinion_words) > 0:
            l, dl = labeling_opinions.get_label()
        json_tweets.append({'tweet_id': str(df_file.at[idx, 'id']), 'tweet': tweet_text,
                            'opinion_words': labeling_opinions.opinion_words, 'c_sentiment': l,
                            'D_sentimet': dl, 'created_at': str(df_file.at[idx, 'created_at']),
                            'date': str(df_file.at[idx, 'date']), 'time': str(df_file.at[idx, 'time'])})

    if en_tweets != 0:
        with codecs.open(des, 'a+', 'utf-8') as fp:
            for jsl in json_tweets:
                fp.write(json.dumps(jsl, ensure_ascii=False))
                fp.write("\n")


""" ------------------------------main area----------------------------------------"""
out_dir = "../out/friends_profile_preprocessed"
users_source_dir = "../got/users_profile"
friends_source_dir = "../got/friends_profile"
threshold = 0.06
set_output_directory()
u_list = open("../out/all_users.txt", 'r')
op_lst = set(opinion_lexicon.words())
processed_count = 0
for u_name in u_list:
    processed_count += 1
    u_name = u_name.rstrip()
    des = out_dir + "/" + u_name + ".txt"
    if os.path.isfile(des) is False:
        process_user_tweets(des, u_name)
        print(str(processed_count))

ut = Utils()
ut.get_al_lfilename_in_folder("txt", out_dir, "../out/valid_friends.txt")
