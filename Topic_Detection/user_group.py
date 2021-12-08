# this file amis to find the similar users and makes link between them
import pandas as pd

user_categories_file = '../out/users_tweets_cats/usercats.txt'
df = pd.read_csv(user_categories_file)
users = df['username'].unique()
for s_user in range(0, len(users)):
    source_user = users[s_user]
    source_user_df = df[df['username'] == source_user]
    num_source = source_user_df.shape[0]
    """
    general_topics might have a  lot of duplicates.this is becuase of multiple topic related words and multiple sub topics
    """
    source_general_topics = source_user_df['general_topic'].tolist()

    for t_user in range(s_user + 1, len(users)):
        target_user = users[t_user]
        target_user_df = df[df['username'] == target_user]
        num_source = source_user_df.shape[0]
        target_general_topics = target_user_df['general_topic'].tolist()
        general_topic_intersects = list(set(source_general_topics) & set(target_general_topics))
        general_topic_unions = set(source_general_topics).union(set(target_general_topics))
        w = len(general_topic_intersects) / len(general_topic_unions)
        if w > 0.1:
            with open('../out/users_tweets_cats/similar_users_w.txt', 'a+') as suf:
                suf.write(source_user + ';' + target_user + ';' + str(w) + '\n')
        else:
            print(w)
