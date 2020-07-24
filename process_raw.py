# -*- coding: utf-8 -*-

"""

@author: alexyang

@contact: alex.yang0326@gmail.com

@file: process_raw.py

@time: 2019/1/5 17:05

@desc: process raw data

"""
import re
import csv
import os
import codecs
import string
import re

import pandas as pd
import xml.etree.ElementTree as ET
from sklearn.model_selection import train_test_split


def remove_punct(text):
    table = str.maketrans("", "", string.punctuation)
    return text.translate(table)


def find_nth(sent, aspect, n):
    count = 0
    words = sent.split(' ')
    for j in range(len(words)):
        if words[j] == aspect:
            count = count + 1
            # print(j)
            # print(words[j])
            index = sum(len(x) + 1 for i, x in enumerate(words)
                        if i < j)
            # print("index", index)
            if (count == n):
                return index


def csv_reader(file):
    data = []
    content, aspect, sentiment, start, end = list(), list(), list(), list(), list()
    with open(file, 'r', encoding="utf8") as csvfile:
        aspectreader = csv.reader(csvfile, delimiter=',')
        j = 0
        count = 0
        for row in aspectreader:
            if (j == 0):
                j = 1
            else:
                sent = row[0].lower()
                sent = remove_punct(sent)
                sent.replace('\d+', '')
                # sent.replace(r'\b\w\b', '').replace(r'\s+', ' ')
                # sent.replace('\s+', ' ', regex=True)
                # sent=re.sub(r"^\s+|\s+$", "", sent), sep='')
                sent = re.sub(r"^\s+|\s+$", "", sent)
                aspects = [x.replace("'", "").replace('[', "").replace("\"", "").replace(']', "").strip().lower() for x
                           in row[1].split(",")]

                while ("" in aspects):
                    aspects.remove("")

                sentiments = [x.strip().replace("'", "").replace('[', "").replace("\"", "").replace(']', "").lower() for
                              x in row[2].split(",")]
                while ("" in sentiments):
                    sentiments.remove("")

                if (len(aspects) == len(sentiments)):
                    for i in range(0, len(aspects)):
                        _aspect = aspects[i]
                        _aspect = remove_punct(_aspect)
                        _aspect.replace('\d+', '')
                        # _aspect.replace(r'\b\w\b', '').replace(r'\s+', ' ')
                        # sent.replace('\s+', ' ', regex=True)
                        # sent=re.sub(r"^\s+|\s+$", "", sent), sep='')
                        _aspect = re.sub(r"^\s+|\s+$", "", _aspect)
                        if len(_aspect.split()) > 1:
                            start_index = sent.find(_aspect)
                            if start_index == -1:
                                print(sent + " - " + _aspect)
                                continue
                            end_index = start_index + len(_aspect)
                        else:

                            if not (any(char.isdigit() for char in aspects[i])):
                                # print(sent + " -" + aspects[i])
                                start_index = find_nth(sent, _aspect, 1)
                                if start_index is None:
                                    count = count + 1
                                    # print(sent+" - "+_aspect)
                                    continue
                                end_index = start_index + len(_aspect)
                            else:
                                # print(sent)
                                # print(aspects[i])
                                _aspect = aspects[i][:-2]
                                # print("len", len(aspects[i][:-2]))
                                # print(_aspect)
                                # print(aspects[i][-1])
                                start_index = find_nth(sent, _aspect, int(aspects[i][-1]))
                                # print(start_index)
                                if start_index is None:
                                    # print(sent+" - "+aspects[i])
                                    continue
                                end_index = start_index + len(aspects[i][:-2])

                                # print(str(start_index)+"+"+str(len(_aspect)))

                        # datam = (sent, aspects[i], sentiments[i],start_index,end_index)
                        # data.append(datam)
                        content.append(sent)
                        aspect.append(_aspect)
                        sentiment.append(sentiments[i])
                        start.append(start_index)
                        end.append(end_index)
                else:
                    print(sent)

        print("count", count)
    return content, aspect, sentiment, start, end


def process_data(file_path, is_train_file, save_folder):
    content, aspect, sentiment, start, end = csv_reader(file_path)
    if not is_train_file:
        test_data = {'content': content, 'aspect': aspect, 'sentiment': sentiment,
                     'from': start, 'to': end}
        test_data = pd.DataFrame(test_data, columns=test_data.keys())
        test_data.to_csv(os.path.join(save_folder, 'train.csv'), index=None)

    # train1_content, test_content, train1_aspect, test_aspect, train1_senti, test_senti, train1_start, test_start, train1_end, test_end = train_test_split(
    #     content, aspect, sentiment, start, end, test_size=0.2)
    #
    # test_data = {'content': test_content, 'aspect': test_aspect, 'sentiment': test_senti, 'from': test_start,
    #              'to': test_end}
    # test_data = pd.DataFrame(test_data, columns=test_data.keys())
    # test_data.to_csv(os.path.join(save_folder, 'test.csv'), index=None)
    #
    # train_content, valid_content, train_aspect, valid_aspect, train_senti, valid_senti, train_start, valid_start, train_end, valid_end = train_test_split(
    #     train1_content, train1_aspect, train1_senti, train1_start, train1_end, test_size=0.1)
    #
    # train_data = {'content': train_content, 'aspect': train_aspect, 'sentiment': train_senti,
    #               'from': train_start, 'to': train_end}
    # train_data = pd.DataFrame(train_data, columns=train_data.keys())
    # train_data.to_csv(os.path.join(save_folder, 'train.csv'), index=None)
    # valid_data = {'content': valid_content, 'aspect': valid_aspect, 'sentiment': valid_senti,
    #               'from': valid_start, 'to': valid_end}
    # valid_data = pd.DataFrame(valid_data, columns=valid_data.keys())
    # valid_data.to_csv(os.path.join(save_folder, 'valid.csv'), index=None)


if __name__ == '__main__':
    process_data('./raw_data/SigmaLaw-ABSA.csv', is_train_file=False, save_folder='./data')

