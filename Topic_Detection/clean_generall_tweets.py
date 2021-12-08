import codecs
import os
import cld2
import pandas as pd

""" ---------------------private method area----------------------------------------"""


def language_detect(tweet_text):
    try:
        isReliable, textBytesFound, details = cld2.detect(tweet_text)
        if (details[0][2] > 50):
            lang = details[0][1]
        else:
            lang = "non"
    except:
        lang = "non"
    return lang


def tweet_size(tweet_text):
    return len(str(tweet_text).split(' '))


def set_output_directory():
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)


def get_file_path(user_name):
    # user might be on of main users or on of main users friends
    if os.path.exists(users_source_dir + '/' + user_name + '.txt'):
        return users_source_dir + '/' + user_name + '.txt'


def process_general_tweets(des_fie, user_name):
    json_tweets = []
    source_file = get_file_path(user_name)
    if source_file==None:
        print(user_name+".txt not exist")
        return
    df_file = pd.read_json(codecs.open(source_file, 'r', 'utf-8'), orient='records', lines=True)
    url_regex = r'(\S+[.]){2,}[^\s]+|\S+:\/\/(\S+[.])+[^\s]+'
    mention_regex = r'@\S+'
    # just number strings we don't want to eliminate 2 from CO2
    number_regex = r'\d\d+'
    non_alphanumeric_regex = r'[^((a-zA-Z0-9)+|\s)]'

    df_file['tweet'] = df_file['tweet'].str.replace(mention_regex + "|" + url_regex + "|" + number_regex, ' ',
                                                    case=False)

    #df_file['tweet'] = df_file['tweet'].str.replace(common_topic_regex, ' ', case=False)
    df_file['Language'] = df_file['tweet'].apply(lambda x: language_detect(x))
    df_file = df_file.drop(df_file.loc[df_file['Language'] != 'en'].index)

    # just words
    df_file['tweet'] = df_file['tweet'].str.replace(non_alphanumeric_regex, ' ', case=False)
    # replace unnecessary white space
    df_file['tweet'] = df_file['tweet'].str.replace(r'(\s)+', ' ', case=False)

    df_file["strLen"] = df_file['tweet'].apply(lambda x: tweet_size(x))
    df_file = df_file.drop(df_file.loc[df_file['strLen'] < 4].index)

    if df_file.index.size >= 0:
        with open(des_fie, 'a+', encoding='utf-8') as file:
            df_file[['tweet']].to_csv(file, encoding='utf-8', header=False, index=False, line_terminator='\n')


""" ------------------------------main area----------------------------------------"""
# Samsung related topics are common between all users so it has no value for detecting similar users
#common_topic_regex = r'(.+samsung).+'
out_dir = "../out/general_profile_preprocessed"
users_source_dir = "../got/users_general_profile"
set_output_directory()
#user_list = open("../out/selected_users.txt", 'r')
user_list = open("../out/valid_friends.txt", 'r')
processed_count = 0
for u_name in user_list:
    processed_count += 1
    u_name = u_name.rstrip()
    des = out_dir + "/" + u_name + ".txt"
    if not os.path.exists(des):
               process_general_tweets(des, u_name)
    print(str(processed_count))
