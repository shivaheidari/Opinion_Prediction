import codecs
import json
import os
from datetime import timedelta
from string import Template
import numpy as np
import pandas as pd
from Utils import Utils


def set_output_directory(out_dir):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)


def is_not_zero_vector(x):
    return any(t != 0.0 for t in x)


def get_stubborness(uname):
    stub_dict = Utils().load_dictionary_with_list_value('../influence_matrix/stubborness.txt')
    return float(stub_dict[uname])


def get_similar_users(user_name):
    hidden_inf_file = '../out/users_tweets_cats/similar_users_w.txt'
    hidden_inf = pd.read_csv(hidden_inf_file, names=['source', 'target', 'score'], sep=';')
    where_user_is_source = list(
        hidden_inf[(hidden_inf['source'] == user_name)].loc[:, ['target', 'score']].values.tolist())
    where_user_is_target = list(
        hidden_inf[(hidden_inf['target'] == user_name)].loc[:, ['source', 'score']].values.tolist())
    all_similars = where_user_is_source + where_user_is_target
    return all_similars


def get_real_neighbors(user_name):
    infscores_df = pd.read_csv('../influence_matrix/infscore.txt', names=["source", "target", "score"], sep=",")
    user_neigbs = infscores_df[(infscores_df['source'] == user_name)]
    return list(user_neigbs.loc[:, ['target', 'score']].values.tolist())


def get_all_friends_df(friends):
    all_friends_df = pd.DataFrame(columns=['created_at', 'vector_influence', 'vector'])
    count = 0
    for friend_sm in friends:
        count = count + 1
        w2v_path = h = w2v_path_template.substitute(name=friend_sm[0])
        if os.path.isfile(w2v_path):
            df_file = pd.read_json(w2v_path, orient='records', lines=True)
            df_file = df_file.drop(df_file.loc[df_file['created_at'] < start_time].index)
            df_file = df_file.drop(df_file.loc[df_file['created_at'] > end_time].index)
            if (df_file.shape[0] > 0):
                print(str(count) + ' -  ' + str(df_file.shape[0]))
                df_file = df_file[df_file['vector'].apply(is_not_zero_vector)]
                df_file['vector_influence'] = df_file['vector'].apply(lambda x: np.multiply(x, friend_sm[1]))
                all_friends_df = all_friends_df.append(df_file[['created_at', 'vector_influence', 'vector']],
                                                       ignore_index=True)
    return all_friends_df


def feature_extraction_original(user_name, time_window):
    json_features = []
    stub = get_stubborness(user_name)
    real_neighbors = get_real_neighbors(user_name)
    real_friends_df = get_all_friends_df(real_neighbors)

    ufile = w2v_path_template.substitute(name=user_name)
    user_df = pd.read_json(ufile, lines=True)
    user_df = user_df.drop(user_df.loc[user_df['created_at'] < start_time].index)
    user_df = user_df.drop(user_df.loc[user_df['created_at'] > end_time].index)
    count = 0
    for idx in user_df.index:
        date = user_df.at[idx, 'created_at']
        count = count + 1
        print(count)
        since = date - timedelta(time_window)

        """-------------------------**history_opinion**--------------------------"""
        user_df_history = user_df[user_df['created_at'] < since]
        personal_histotry = [sum(col) for col in zip(*user_df_history['vector'])]
        if len(personal_histotry) == 0:
            personal_histotry = pr = np.zeros(w2veclen).tolist()

        history_real_neighbor_df = real_friends_df[real_friends_df['created_at'] < since]
        if len(history_real_neighbor_df['vector']) == 0:
            history_neighbors_influence = pr = np.zeros(w2veclen)
        else:
            history_neighbors_influence = [sum(col) for col in zip(*history_real_neighbor_df['vector'])]

        history_opinion_influence = np.add(history_neighbors_influence, personal_histotry)

        """-------------------------**personal_prior**--------------------------"""
        user_df_prior = user_df[(user_df['created_at'] < date) & (user_df['created_at'] >= since)]
        vec_sum = [sum(col) for col in zip(*user_df_prior['vector'])]
        personal_prior = np.multiply(stub, vec_sum)
        if (len(personal_prior) == 0):
            personal_prior = pr = np.zeros(w2veclen)

        """-------------------------**real_neighbors_influence**--------------------------"""
        real_neighbor_df = real_friends_df[
            (real_friends_df['created_at'] < date) & (real_friends_df['created_at'] >= since)]
        if len(real_neighbor_df['vector_influence'].tolist()) == 0:
            neighbors_influence = pr = np.zeros(w2veclen)
        else:
            neighbors_influence = real_neighbor_df['vector_influence'].sum()

        json_features.append(
            {'tweet_id': str(user_df.at[idx, 'tweet_id']), 'timestamp': str(user_df.at[idx, 'created_at']),
             'c_sentiment': str(user_df.at[idx, 'c_sentiment']),
             'D_sentiment': str(user_df.at[idx, 'D_sentimet']), 'date': str(user_df.at[idx, 'date']),
             'time': str(user_df.at[idx, 'time']), 'personal_prior': personal_prior.tolist(),
             "history_opinion_influence": history_opinion_influence.tolist(),
             'real_neighbors_influence': neighbors_influence.tolist()})

    output_file_path = original_output_template.substitute(name=user_name)
    with codecs.open(output_file_path, 'w', 'utf-8') as fp:
        for jsl in json_features:
            fp.write(json.dumps(jsl, ensure_ascii=False))
            fp.write("\n")


def feature_hidden(user_name, time_window):
    json_features = []
    stub = get_stubborness(user_name)
    similar_users = get_similar_users(user_name)
    similar_friends_df = get_all_friends_df(similar_users)

    ufile = w2v_path_template.substitute(name=user_name)
    user_df = pd.read_json(ufile, lines=True)
    user_df = user_df.drop(user_df.loc[user_df['created_at'] < start_time].index)
    user_df = user_df.drop(user_df.loc[user_df['created_at'] > end_time].index)
    count = 0
    for idx in user_df.index:
        date = user_df.at[idx, 'created_at']
        count = count + 1
        print(count)
        since = date - timedelta(time_window)

        """-------------------------**personal_histotry**--------------------------"""
        user_df_history = user_df[user_df['created_at'] < since]
        personal_histotry = [sum(col) for col in zip(*user_df_history['vector'])]
        if len(personal_histotry) == 0:
            personal_histotry = pr = np.zeros(w2veclen).tolist()

        """-------------------------**personal_prior**--------------------------"""
        user_df_prior = user_df[(user_df['created_at'] < date) & (user_df['created_at'] >= since)]
        vec_sum = [sum(col) for col in zip(*user_df_prior['vector'])]
        personal_prior = np.multiply(stub, vec_sum)
        if (len(personal_prior) == 0):
            personal_prior = pr = np.zeros(w2veclen)

        """-------------------------**hidden_community**--------------------------"""
        sate_neighbor_df = similar_friends_df[
            (similar_friends_df['created_at'] < date) & (similar_friends_df['created_at'] >= since)]
        if len(sate_neighbor_df['vector_influence'].tolist()) == 0:
            hidden_community_inf = np.zeros(w2veclen)
        else:
            hidden_community_inf = sate_neighbor_df['vector_influence'].sum()

        json_features.append(
            {'tweet_id': str(user_df.at[idx, 'tweet_id']), 'timestamp': str(user_df.at[idx, 'created_at']),
             'c_sentiment': str(user_df.at[idx, 'c_sentiment']),
             'D_sentiment': str(user_df.at[idx, 'D_sentimet']), 'date': str(user_df.at[idx, 'date']),
             'time': str(user_df.at[idx, 'time']), 'personal_prior': personal_prior.tolist(),
             'personal_history': personal_histotry, 'hidden_community_inf': hidden_community_inf.tolist()})

    output_file_path = hidden_output_template.substitute(name=user_name)
    with codecs.open(output_file_path, 'w', 'utf-8') as fp:
        for jsl in json_features:
            fp.write(json.dumps(jsl, ensure_ascii=False))
            fp.write("\n")


hidden_output_template = Template('../out/feature_hidden/$name.json')
original_output_template = Template('../out/feature_orginal/$name.json')

set_output_directory('../out/feature_hidden')
set_output_directory('../out/feature_orginal')

w2v_dir = ''
time_window = 10
w2veclen = 200
w2v_path_template = Template('../out/word2vec_glove_friends/$name.json')
start_time = pd.to_datetime('2019-03-01')
end_time = pd.to_datetime('2019-06-30')
user_list = Utils().csv_read_one_col("../out/opinion_perMonth/main_nodelist.txt")
for user in user_list:
    if not os.path.exists(original_output_template.substitute(name=user)):
        feature_extraction_original(user, time_window)
for user in user_list:
    if not os.path.exists(hidden_output_template.substitute(name=user)):
        feature_hidden(user, time_window)