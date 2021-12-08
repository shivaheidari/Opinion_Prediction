import codecs
import datetime
import enum
import os
import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta
from Utils import Utils


class report_types(enum.Enum):
    full = 1
    main_users = 2


def get_report_df(report_type, report_file, selected_users):
    mydateparser = lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
    report_df = pd.read_csv(report_file, parse_dates=['date'], date_parser=mydateparser)
    if report_type == report_types.full:
        return report_df
    else:
        user_list = Utils().csv_read_one_col(selected_users)
        return report_df[report_df['user'].isin(user_list)]


def get_users_in_selected_time(report_df, selected_month):
    selected_month.sort()
    start_date = selected_month[0]
    end_date = (selected_month[len(selected_month) - 1]) + relativedelta(months=+1)
    report_df = report_df.loc[(report_df['date'] < end_date) & (report_df['date'] >= start_date)]
    return list(report_df.loc[report_df['count'] > 0]['user'].unique())

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

class select_best_time:
    class user_per_month_report:
        def __init__(self, minimum_all_users, minimum_main_users, report_file, selected_users, users_source_dir):
            self.minimum_all_users = minimum_all_users
            self.minimum_main_users = minimum_main_users
            self.report_file = report_file
            self.selected_users = selected_users
            self.users_source_dir = users_source_dir

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
