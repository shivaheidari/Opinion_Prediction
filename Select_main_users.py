import os
from pathlib import Path
import glob
import csv


def set_output_directory(out_dir):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

def csv_read(filename):
    list_of_rows = []
    with open(filename, 'r') as read_obj:
        csv_reader = csv.reader(read_obj)
        list_of_rows = list(csv_reader)
    return list_of_rows


def save_list(lst, filename):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        for item in lst:
            writer.writerow([item])


def save_list_2(lst, filename, header):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(lst)


def get_all_filename_in_folder(format, path, out_filename):
    files_path = [f for f in glob.glob(path + "**/*." + format, recursive=False)]
    lst = []
    for file in files_path:
        lst.append(Path(file).stem)
    save_list(lst, out_filename)
    return lst


set_output_directory("out/user_friends")

# ListOf users how are in folloewee folder
users = get_all_filename_in_folder('txt', 'got/followee', "out/in_followee.csv")

# source->follows->target
edge_list = []
friends_count = []
# userFriends
for user in users:
    friends_lst = []
    followee_file = 'got/followee/' + user + '.txt'
    user_followee = []
    if os.path.exists(followee_file):
        user_followee = list(csv.reader(open(followee_file)))

    for u_followee in user_followee:
        if len(u_followee) > 0:
            ufr = u_followee[0]
            if (os.path.exists('got/friends_profile/' + ufr + '.txt') or os.path.exists(
                    'got/users_profile/' + ufr + '.txt')):
                if ufr not in friends_lst:
                    friends_lst.append(ufr)
                    edge_list.append([str(user).lower(), str(ufr).lower()])

    friends_count.append([user, len(friends_lst)])
    if len(friends_lst):
        save_list(friends_lst, "out/user_friends/" + user + ".txt")

save_list_2(edge_list, "out/edgelist.txt", ['source', 'target'])
# لیست کاربران اصلی انتخاب شده
get_all_filename_in_folder('txt', 'out/user_friends', "out/selected_users.txt")
#  لیست تمامی کاربران و دوستانشان که انتخاب شده اند
all_users = list(set([i[1] for i in edge_list]).union(set([i[0] for i in edge_list])))
save_list(all_users, "out/all_users.txt")
# friends_count is a report
# save_list_2(friends_count,"friends_count.csv",['user','friends'])


"""
f1=Utils().get_al_lfilename_in_folder("txt","D:\\gof_sentiment\\got\\users_general_profile","got_ug.txt")
f2 = Utils().get_al_lfilename_in_folder('txt', 'D:\\gof_sentiment\\got\\followee', "got_flee.txt")
m=list(set(f1) & set(f2))
"""