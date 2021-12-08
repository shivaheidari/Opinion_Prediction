import codecs
import datetime
import enum
import os
import pandas as pd
from dateutil.relativedelta import relativedelta
from Utils import Utils


class report_types(enum.Enum):
    full = 1
    main_users = 2


""" ---------------------private method area----------------------------------------"""


def get_users_in_selected_time(report_df, selected_month):
    selected_month.sort()
    start_date = selected_month[0]
    end_date = (selected_month[len(selected_month) - 1]) + relativedelta(months=+1)
    report_df = report_df.loc[(report_df['date'] < end_date) & (report_df['date'] >= start_date)]
    return list(report_df.loc[report_df['count'] > 0]['user'].unique())


def set_output_directory():
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)


def get_report_df(report_type):
    mydateparser = lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
    report_df = pd.read_csv(report_file, parse_dates=['date'], date_parser=mydateparser)
    if report_type == report_types.full:
        return report_df
    else:
        user_list = Utils().csv_read_one_col(selected_users)
        return report_df[report_df['user'].isin(user_list)]


def get_file_path(user_name):
    if os.path.exists(users_source_dir + '/' + user_name + '.txt'):
        return users_source_dir + '/' + user_name + '.txt'
    else:
        return "-1"


def fill_with_neighbour_month(month_list, month_count, report_type):
    report_df = get_report_df(report_type)
    while True:
        month_list.sort()
        min_month = month_list[0]
        max_month = month_list[len(month_list) - 1]
        prev_month = min_month - relativedelta(months=+1)
        next_month = max_month + relativedelta(months=+1)
        prev_count = len(get_users_in_selected_time(report_df, month_list + [prev_month]))
        next_count = len(get_users_in_selected_time(report_df, month_list + [next_month]))

        if prev_count > next_count:
            month_list.append(prev_month)
        else:
            month_list.append(next_month)

        if len(month_list) >= month_count:
            break


def add_next_neighbour_month(month_list, month_count, report_type):
    report_df = get_report_df(report_type)
    while True:
        month_list.sort()
        max_month = month_list[len(month_list) - 1]
        next_month = max_month + relativedelta(months=+1)
        month_list.append(next_month)
        if len(month_list) >= month_count:
            break


def select_best_n_month(month_count):
    full_report_df = get_report_df(report_types.full)
    main_uers_report_df = get_report_df(report_types.main_users)

    month_uniq = full_report_df['date'].unique()
    month_uniq.sort()
    idx = 0
    while True:
        selected_months = [pd.to_datetime(str(month_uniq[idx])).replace(tzinfo=None)]
        if len(selected_months) < month_count:
            add_next_neighbour_month(selected_months, month_count, report_types.full)
            # fill_with_neighbour_month(selected_months,month_count,report_types.full)

        selected_users = get_users_in_selected_time(main_uers_report_df, selected_months)
        all_selected_users = get_users_in_selected_time(full_report_df, selected_months)
        month_count_reports.append([selected_months, len(selected_users), len(all_selected_users)])
        print(str(selected_months) + " - " + str(len(selected_users)) + " - " + str(len(all_selected_users)) + "\n")
        idx += 1
        if ((len(selected_users) > minimum_main_users) and (len(all_selected_users) > minimum_all_users)) or (
                idx + 2 > len(month_uniq)):
            break

    return selected_months, len(selected_users), len(all_selected_users)


def Convert_to_list(selected_months):
    main_users_list = Utils().csv_read_one_col(selected_users)
    selected_months.sort()
    start_date = selected_months[0]
    end_date = (selected_months[len(selected_months) - 1]) + relativedelta(months=+1)
    print("start converting selected to list....")
    report_df = get_report_df(report_types.full)
    selected_time_users = get_users_in_selected_time(report_df, selected_months)
    final_users=[]
    user_count = 0
    for user_name in selected_time_users:
        user_name = user_name.rstrip()
        source_file = get_file_path(user_name)
        if source_file == "-1":
            continue
        df_file = pd.read_json(codecs.open(source_file, 'r', 'utf-8'), orient='records', lines=True)
        df_date = df_file.loc[(df_file['created_at'] < end_date) & (df_file['created_at'] > start_date)]
        if((user_name in main_users_list) and(df_date.shape[0] >4)) or ((user_name not in main_users_list) and(df_date.shape[0] >1)):
            final_users.append(user_name)
            with open(out_dir + '/opinion.txt', 'a+', encoding='utf-8', newline='') as file:
                df_date.insert(1, "name", ([user_name] * df_date.shape[0]), True)
                df_date['date'] = df_date['created_at'].apply(lambda x: int(x.value * 1e-9))
                df_date[['name', 'date', 'c_sentiment']].to_csv(file, index=False, header=False)
        print(user_count)
        user_count += 1
    return final_users


def save_selected_node_list(final_selected_users):
    Utils().save_list(final_selected_users, out_dir + '/all_nodelist.txt')
    users_list = Utils().csv_read_one_col(selected_users)
    main_users = list(set(final_selected_users)&set(users_list))
    Utils().save_list(main_users, out_dir + '/main_nodelist.txt')


def update_edge_list():
    all_selected_users = Utils().csv_read_one_col(out_dir + '/all_nodelist.txt')
    with  open("../out/edgelist.txt", "r", encoding='utf-8') as edg:
        edgeList = edg.read().splitlines()
    with open(out_dir + "/final-edgelist.txt", 'w') as ef:
        for edge in edgeList:
            nodes = edge.split(',');
            if (nodes[0] in all_selected_users and nodes[1] in all_selected_users):
                ef.write(edge + "\n")


""" ------------------------------main area----------------------------------------"""

minimum_main_users = 300
minimum_all_users = 1500
all_valid_users = "../out/valid_friends.txt"
out_dir = "../out/opinion_perMonth"
report_file = out_dir + '/report.txt'
users_source_dir = '../out/friends_profile_preprocessed'
selected_users = "../out/selected_users.txt"
set_output_directory()
user_list = Utils().csv_read(all_valid_users)
start_date = datetime.datetime.strptime('2016-01-01', '%Y-%m-%d')
end_date = datetime.datetime.strptime('2020-03-30', '%Y-%m-%d')

month_count_reports = []
"""
usp_rpt = user_per_month_report(report_file, out_dir, start_date, end_date, users_source_dir)
usp_rpt.process_all(user_list)



for month_count in range(1, 6):
    selected_months, users_count, all_selected_users = select_best_n_month(month_count)
    if (users_count >= minimum_main_users) and (len(all_selected_users) > minimum_all_users):
        break

Utils().save_list(month_count_reports, out_dir + '/selected_count_report.txt')
month_count_reports = np.array(month_count_reports)
# یه متد بنویسم که از حداقل ها 10 تا 10 تا و صدتا صد تا کم کنه تا بهینه پیدا شه
# الان انتخاب دستی هست.
final_select = month_count_reports[np.argmax(month_count_reports[:, 1]), :]
"""
final_select = [[pd.to_datetime('2019-04-01'), pd.to_datetime('2019-05-01'), pd.to_datetime('2019-06-01')]]
final_users = Convert_to_list(final_select[0])

save_selected_node_list(final_users)

update_edge_list()
