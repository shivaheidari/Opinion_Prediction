from Topic_Detection.text_topic_detection import text_topic_detection
from Topic_Detection.summerize_local_topics import summarize_local_topics
from Utils import Utils
import os


def set_output_directory():
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)


out_dir = "../out/topics/"
set_output_directory()
general_tweets_text_dir = "../out/general_profile_preprocessed/"
lda_topic_file = "../out/topics/out.txt"
summarized_topic_file = "../out/topics/summary.txt"
user_list = Utils().csv_read('../out/valid_friends.txt')
text_topic_detection(general_tweets_text_dir, lda_topic_file, user_list).get_lda_topics()
summarize_local_topics(lda_topic_file, summarized_topic_file).summarize_user_topics()
