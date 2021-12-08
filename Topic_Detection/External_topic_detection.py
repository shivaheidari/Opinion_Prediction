from Topic_Detection.meaning_cloud_topic_detection import meaning_cloud_topic_detection
import pandas as pd
import Utils

model = 'IAB_en'
license_key = '0e6774ce12e99c6a171bffc360a6a1f0'
local_topics = "../out/topics/summary.txt"
resulted_topics_categories = '../out/users_tweets_cats/cats.txt'
all_users_topics = "../out/topics/out.txt"
user_categories_file = '../out/users_tweets_cats/usercats.txt'

"""
call meaning cloud to get categories for uniq list of topical words. 
topical words are summary of lda topic detection results for all users. 
"""
# m_cloud = meaning_cloud_topic_detection(model, license_key, local_topics, resulted_topics_categories)
# m_cloud.call_meaning_cloud()

processed = 0
"""
get each user topical categories with matching user lda topics and the categories that obtained from meaning cloud
output is: 'username','general_topic','sub_topic'
"""
cats = pd.read_csv(resulted_topics_categories, sep=';')
cats = cats.drop(cats.loc[cats['topic'] == 'Uncategorized'].index)

users_categories = []
with open(all_users_topics) as sf:
    for line in sf:

        t_data = str(line).split(':')

        user_name = t_data[0]
        user_terms = str(t_data[1]).replace(" ", "").split(',')
        user_topics = cats[cats['term'].isin(user_terms)]
        for ut in user_topics['topic']:
            cat = str(ut).split('>')
            general_cat = cat[0]
            sub_cat = cat[1] if len(cat) > 1 else " "
            users_categories.append([user_name, general_cat, sub_cat])
        processed += 1
        print(processed)

Utils.Utils().save_list_2(users_categories, user_categories_file, ['username', 'general_topic', 'sub_topic'])
