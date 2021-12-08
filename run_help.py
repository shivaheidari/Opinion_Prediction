"""
1-run select_main_users.py to get main users how has at least 1 friend in folowee folder
2-run preProcessing/Pre_proccessing_data.py to clean data and get sentiment score
3-run WordEmbeding/Word_Embeding to get vector presentation of opinion words ***- resulted vector is sum of all opinion
      words vectors
4-run topic detection/clean_general_tweets to filter language unwanted string like urls,numbers,user names that mentions
      in the  text and etc
5-run topic_detection/local_topic_detection.py to run lda and get user topics then summarize all topics that belong to
      more than one users and save uniq topic word list
6-run topic_detection/External_topic_detection to call meaning_cloud and get topic categories for uniq topic word list
      resulted in step 5 then for each users determine categories according to their topic words
7-run topic-detection/user_group.py to get similar users base on users topics from previous step. it'll be save in
similar_users_w.txt and each line will be like node1,node2,similarity_score
8- run best_time_period.py to get files that contains list of node and opinions and edges. this files will be used in
next step. selecting shortest time period that contains the most users tweets data
8- get stuberness and real influence score by running aslm and copy the results to influence_matrix in the root path
9-run feature_extraction.py. limiting time by start_time and end_time will improve performance. for start_time one month
 before the time period that has been selected in step 8,will be a good choice.
 feature _extraction will be run on main users that selected in step 8.

"""