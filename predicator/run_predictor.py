from string import Template
from ..Utils import Utils
from predictor import predictor
import enum
import os


class method_types(enum.Enum):
    GRU = 1
    Classic = 2
    LSTM=3
    RNN=4


main_user_file = "../out/opinion_perMonth/main_nodelist.txt"


def set_output_directory(out_dir):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

def run_method(method_type, train_lst, history_lst, iteration, feature_file_template, dataset_fileds, output_file_name):
    general_accuracy = []
    general_f1 = []
    for train in train_lst:
        for hist in history_lst:
            for iter in range(0, iteration):
                f1_summation = 0
                acc_summation = 0
                nbuser = 0
                user_list = Utils().csv_read_one_col(main_user_file)
                for uname in user_list:
                    print(uname)
                    uname = uname.rstrip()
                    prediction_obj = predictor(uname, feature_file_template, dataset_fileds)
                    if method_type == method_types.Classic:
                        loss_score, acc, f1_sc, train_set_len, test_set_len = prediction_obj.run_Classic_classifier(
                            train, hist)
                    elif method_type==method_types.RNN:
                        loss_score, acc, f1_sc, train_set_len, test_set_len = prediction_obj.run_simplernn(train, hist)

                    elif method_type==method_type.LSTM:
                        loss_score, acc, f1_sc, train_set_len, test_set_len = prediction_obj.run_LSTM(train, hist)

                    else:
                        loss_score, acc, f1_sc, train_set_len, test_set_len = prediction_obj.run_GRU(train, hist)

                    sent = uname + ';' + str(acc) + ';' + str(f1_sc) + ';' + str(loss_score) + ';' + str(
                        train_set_len) + ';' + str(test_set_len)
                    fre = open(output_file_name, 'a+')
                    fre.write(sent)
                    fre.write("\n")
                    fre.close()
                    f1_summation += float(f1_sc)
                    acc_summation += float(acc)
                    nbuser += 1

                avg = f1_summation / nbuser
                avg_acc = acc_summation / nbuser
                general_accuracy.append(avg_acc)
                general_f1.append(avg)
                print(general_f1)
                print(general_accuracy)

    return general_f1, general_accuracy


def save_report(report_file, general_accuracy, general_f1):
    with open(report_file, 'a+') as rf:
        rf.write(str(general_accuracy))
        rf.write("\n")
        rf.write(str(general_f1))


def run_chen():
    trains = [90]
    history = [10000]
    iteration = 5
    general_feature_file_template = Template('../out/feature_orginal/$name.json')
    dataset_fileds = ['personal_prior', 'real_neighbors_influence', 'history_opinion_influence']
    outpu_file = ('../out/chen/chen_details.txt')
    general_f1, general_accuracy = run_method(method_types.GRU,trains, history, iteration, general_feature_file_template, dataset_fileds,
                                              outpu_file)
    report_file = '../out/chen/report.txt'
    save_report(report_file, general_accuracy, general_f1)


def run_hidden(trains, history, outpu_file, report_file, iteration):
    dataset_fileds = ['personal_prior', 'personal_history', 'hidden_community_inf']
    hidden_feature_file_template = Template('../out/feature_hidden/$name.json')
    general_f1, general_accuracy = run_method(method_types.GRU,trains, history, iteration, hidden_feature_file_template, dataset_fileds,
                                              outpu_file)
    # general_f1, general_accuracy = run_method(method_types.LSTM, trains, history, iteration,
    #                                           hidden_feature_file_template, dataset_fileds,
    #                                           outpu_file)
    # general_f1, general_accuracy = run_method(method_types.RNN, trains, history, iteration,
    #                                           hidden_feature_file_template, dataset_fileds,
    #                                           outpu_file)
    save_report(report_file, general_accuracy, general_f1)


def run_classic():
    trains = [90]
    history = [10000]
    iteration = 5
    dataset_fileds = ['personal_prior', 'personal_history', 'hidden_community_inf']
    hidden_feature_file_template = Template('../out/feature_hidden/$name.json')
    outpu_file = ('../out/classic/classic_hidden_details.txt')
    general_f1, general_accuracy = run_method(method_types.Classic,trains, history, iteration, hidden_feature_file_template, dataset_fileds,
                                              outpu_file)
    report_file = '../out/classic/report.txt'
    save_report(report_file, general_accuracy, general_f1)

set_output_directory('../out/classic')
set_output_directory('../out/hidden')
set_output_directory('../out/chen')

run_hidden([90], [10000], '../out/hidden/itr_5_hidden_details.txt', '../out/hidden/itr_5_hidden_reports.txt', 5)
# run_chen()

#run_hidden([90],[10, 25, 40, 65, 80],'../out/hidden/history_hidden_details.txt','../out/hidden/history_hidden_reports.txt',1)
#run_hidden([60, 70, 80, 90], [10000], '../out/hidden/trains_hidden_details.txt',
          # '../out/hidden/trains_hidden_reports.txt', 1)
#run_classic()


