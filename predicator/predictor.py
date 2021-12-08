import gc

import numpy as np
import pandas as pd
from keras import backend as K
from keras.layers import Dense, GRU, Dropout,LSTM,SimpleRNN
from keras.models import Sequential
from keras.utils import np_utils
from sklearn import tree
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split

"""------------------****private_methods***--------------------"""


def get_categorical(label):
    uniques, ids = np.unique(label, return_inverse=True)
    y_code = np_utils.to_categorical(ids, len(uniques))
    return y_code, uniques


def reverse(uniques, y_code):
    m = y_code.argmax(1)
    return uniques[m]


def get_reverse_predict(predicted, uniques_label):
    if uniques_label.shape[0] == 1:
        reverse_pred = predicted
    else:
        reverse_pred = uniques_label[list(predicted)]
    return reverse_pred


def get_model(loss, outlayer, test_label, test_set, train_label, train_set):
    model = Sequential()
    model.add(GRU(3, input_shape=(3, 200), return_sequences=True))
    # model.add(Dropout(0.2))
    # model.add(GRU(3, return_sequences=True))
    # model.add(Dropout(0.2))
    # model.add(GRU(3, return_sequences=True))
    # model.add(Dropout(0.1))
    # model.add(GRU(3, return_sequences=True))
    model.add(GRU(3, return_sequences=False))
    model.add(Dense(outlayer, activation='softmax'))
    model.compile(optimizer='Adam', loss=loss, metrics=['accuracy'])
    model.fit(train_set, train_label, epochs=10, validation_data=(test_set, test_label))
    model.predict(test_set, verbose=0)
    return model

def get_lstm_model(loss, outlayer, test_label, test_set, train_label, train_set):
    model = Sequential()
    model.add(LSTM(3, input_shape=(3, 200), return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(3, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(3, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(3, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(3, return_sequences=False))
    model.add(Dense(outlayer, activation='softmax'))
    model.compile(optimizer='Adam', loss=loss, metrics=['accuracy'])
    model.fit(train_set, train_label, epochs=10, validation_data=(test_set, test_label))
    model.predict(test_set, verbose=0)
    return model

def get_rnn_model(loss, outlayer, test_label, test_set, train_label, train_set):
    model = Sequential()
    model.add(SimpleRNN(3, input_shape=(3, 200), return_sequences=True))
    model.add(Dropout(0.2))
    model.add(SimpleRNN(3, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(SimpleRNN(3, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(SimpleRNN(3, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(SimpleRNN(3, return_sequences=False))
    model.add(Dense(outlayer, activation='softmax'))
    model.compile(optimizer='Adam', loss=loss, metrics=['accuracy'])
    model.fit(train_set, train_label, epochs=10, validation_data=(test_set, test_label))
    model.predict(test_set, verbose=0)
    return model

def get_loss(train_label):
    loss = 'categorical_crossentropy'
    out_layer = 3
    if train_label.shape[1] == 2:
        out_layer = 2
        loss = 'binary_crossentropy'
    if train_label.shape[1] == 1:
        loss = "sparse_categorical_crossentropy"
        out_layer = 2
    return loss, out_layer


def get_test_train(train, user_name, feature_file_template, history_len, dataset_filds):
    feature_file = feature_file_template.substitute(name=user_name)
    user_df = pd.read_json(feature_file, lines=True)
    tweets_number = user_df.shape[0]
    if tweets_number < 10:
        train = 50
    train_per = train / 100
    user_df.sort_values(by='timestamp', ascending=True)
    dataset = user_df.head(history_len)[dataset_filds].to_numpy()


    label = user_df.head(history_len)['D_sentiment'].tolist()
    dummy_y, uniques_label = get_categorical(label)
    train_set, test_set, train_label, test_label = train_test_split(dataset, dummy_y, train_size=train_per,
                                                                    shuffle=False)
    for i in range(0, train_set.shape[0]):
        for j in range(0, train_set.shape[1]):
            st = train_set[i][j]
            train_set[i][j] = np.array(st)
    for i in range(0, test_set.shape[0]):
        for j in range(0, test_set.shape[1]):
            st = test_set[i][j]
            test_set[i][j] = np.array(st)
    out = np.concatenate(train_set).ravel()
    out = np.concatenate(out).ravel()
    outtest = np.concatenate(test_set).ravel()
    outtest = np.concatenate(outtest).ravel()
    train_set = out.reshape(train_set.shape[0], train_set.shape[1], 200)
    test_set = outtest.reshape(test_set.shape[0], test_set.shape[1], 200)
    return test_label, test_set, train_label, train_set, uniques_label


"""------------------****main_class***--------------------"""


class predictor:
    def __init__(self, user_name, feature_file_template, dataset_fileds):
        self.user_name = user_name
        self.feature_file_template = feature_file_template
        self.dataset_fileds = dataset_fileds

    def run_GRU(self, train, history_len):
        test_label, test_set, train_label, train_set, uniques_label = get_test_train(train, self.user_name,
                                                                                     self.feature_file_template,history_len,
                                                                                     self.dataset_fileds)
        loss, out_layer = get_loss(train_label)
        model = get_model(loss, out_layer, test_label, test_set, train_label, train_set)
        predicted = model.predict_classes(test_set)
        loss_score, acc = model.evaluate(test_set, test_label)
        reverse_test = reverse(uniques_label, test_label)
        reverse_pred = get_reverse_predict(predicted, uniques_label)
        f1_sc = f1_score(reverse_test, reverse_pred, average='weighted')
        del model
        gc.collect()
        K.clear_session()
        return loss_score, acc, f1_sc, len(train_set), len(test_set)
    def run_LSTM(self,train,history_len):
        test_label, test_set, train_label, train_set, uniques_label = get_test_train(train, self.user_name,
                                                                                     self.feature_file_template,history_len,
                                                                                     self.dataset_fileds)
        loss, out_layer = get_loss(train_label)
        model = get_lstm_model(loss, out_layer, test_label, test_set, train_label, train_set)
        predicted = model.predict_classes(test_set)
        loss_score, acc = model.evaluate(test_set, test_label)
        reverse_test = reverse(uniques_label, test_label)
        reverse_pred = get_reverse_predict(predicted, uniques_label)
        f1_sc = f1_score(reverse_test, reverse_pred, average='weighted')
        del model
        gc.collect()
        K.clear_session()
        return loss_score, acc, f1_sc, len(train_set), len(test_set)
    def run_simplernn(self,train,history_len):
        test_label, test_set, train_label, train_set, uniques_label = get_test_train(train, self.user_name,
                                                                                     self.feature_file_template,
                                                                                     history_len,
                                                                                     self.dataset_fileds)
        loss, out_layer = get_loss(train_label)
        model = get_rnn_model(loss, out_layer, test_label, test_set, train_label, train_set)
        predicted = model.predict_classes(test_set)
        loss_score, acc = model.evaluate(test_set, test_label)
        reverse_test = reverse(uniques_label, test_label)
        reverse_pred = get_reverse_predict(predicted, uniques_label)
        f1_sc = f1_score(reverse_test, reverse_pred, average='weighted')
        del model
        gc.collect()
        K.clear_session()
        return loss_score, acc, f1_sc, len(train_set), len(test_set)



    def run_Classic_classifier(self, train, history_len):
        test_label, test_set, train_label, train_set, uniques_label = get_test_train(train, self.user_name,
                                                                                     self.feature_file_template,history_len,
                                                                                     self.dataset_fileds)
        nsamples, nx, ny = train_set.shape
        d2_train_dataset = train_set.reshape((nsamples, nx * ny))
        classifier = tree.DecisionTreeClassifier()
        classifier.fit(d2_train_dataset, train_label)
        nsamples, nx, ny = test_set.shape
        d2_test_set = test_set.reshape((nsamples, nx * ny))
        predicted = classifier.predict(d2_test_set)
        acc = accuracy_score(test_label, predicted)
        f1_sc = f1_score(test_label, predicted, average='weighted')
        return 0.0,acc, f1_sc, len(train_set), len(test_set)
