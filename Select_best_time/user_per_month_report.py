import codecs
import os
import pandas as pd
from dateutil.relativedelta import relativedelta


def get_file_path(user_name, users_source_dir):
    if os.path.exists(users_source_dir + '/' + user_name + '.txt'):
        return users_source_dir + '/' + user_name + '.txt'
    else:
        return "-1"


def process_opinion_counts(user_name, start_date, report_file, end_date, users_source_dir):
    source_file = get_file_path(user_name, users_source_dir)
    if source_file == "-1":
        return
    df_file = pd.read_json(codecs.open(source_file, 'r', 'utf-8'), orient='records', lines=True)
    df_file['name'] = df_file.apply(lambda x: user_name, axis=1)
    s = start_date
    print(min(df_file['created_at']))
    while True:
        e = s + relativedelta(months=+1)
        df_date = df_file.loc[(df_file['created_at'] < e) & (df_file['created_at'] > s)]
        with open(report_file, 'a+', encoding='utf-8') as r_file:
            r_file.write(user_name + "," + str(s) + "," + str(df_date.shape[0]))
            r_file.write('\n')
        s = e
        if s > end_date:
            break


class user_per_month_report:
    def __init__(self, report_file, out_dir, start_date, end_date, users_source_dir):
        self.report_file = report_file
        self.out_dir = out_dir
        self.start_date = start_date
        self.end_date = end_date
        self.users_source_dir = users_source_dir

    def process_all(self, user_list):
        with open(self.report_file, 'w', encoding='utf-8') as r_file:
            r_file.write("user,date,count")
            r_file.write('\n')
        processed_count = 0
        for user_name in user_list:
            processed_count += 1
            user_name = user_name[0].rstrip()
            des = self.out_dir + "/" + user_name + ".txt"
            process_opinion_counts(user_name, self.start_date, self.report_file, self.end_date, self.users_source_dir)
            print(str(processed_count))
