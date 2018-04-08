from subprocess import Popen, PIPE, STDOUT
from os import listdir
from os.path import isfile, join
import calendar
import datetime
import time
import numpy as np
from multiprocessing import Process
import os

PATH = "stanford-corenlp/"
article_path = 'articles'
#
onlyfiles = [f for f in listdir(article_path) if isfile(join(article_path, f))]

def parse_sentiment_to_text(fileArr):
    for idx, file in enumerate(fileArr):
        sentiment_bin = [0 for i in range(5)]
        proc = Popen(['java','-cp', "stanford-corenlp/*", '-mx5g',
        'edu.stanford.nlp.sentiment.SentimentPipeline', '-file', join(article_path, file)],
        stdout=PIPE, stdin=PIPE)
        out = proc.communicate()[0]
        lines = out.split(b'\n')
        for i, line in enumerate(lines):
            line = line.strip()
            if i % 2 != 0:
                if line == b"Very negative":
                    sentiment_bin[0] = sentiment_bin[0] + 1
                if line == b"Negative":
                    sentiment_bin[1] = sentiment_bin[1] + 1
                if line == b"Neutral":
                    sentiment_bin[2] = sentiment_bin[2] + 1
                if line == b"Positive":
                    sentiment_bin[3] = sentiment_bin[3] + 1
                if line == b"Very positive":
                    sentiment_bin[4] = sentiment_bin[4] + 1

        sentiment_bin = np.array(sentiment_bin)
        dateStr = file.split('.')[0]
        timestamp = calendar.timegm(time.strptime(dateStr, '%b_%d_%Y__%H_%M'))
        max_sentiment = np.argmax(sentiment_bin)
        if timestamp >= 1417412036:
            if not os.path.exists('sentiments/'):
                os.makedirs('sentiments/')
            with open('sentiments/' + str(timestamp) + '.txt', 'w') as sf:
                sf.write(str(timestamp) + ',' + str(max_sentiment - 2) + '\n')

processes = []


# for i in range(8):
#     print(i * round(len(onlyfiles) / 8))
#     print((i + 1) * round(len(onlyfiles) / 8) - 1)
#     p = Process(target=parse_sentiment_to_text, args=(onlyfiles[i * round(len(onlyfiles) / 8) : (i + 1) * round(len(onlyfiles) / 8) - 1], ))
#     processes.append(p)
#     p.start()


def parse_txt_to_csv():
    onlyfiles = [f for f in listdir('sentiments') if isfile(join('sentiments', f))]
    with open('sentiments.csv', 'w') as sentimentCSV:
        for i in range(len(onlyfiles)):
            with open(join('sentiments', onlyfiles[i]), 'r') as st:
                sentimentCSV.write(st.read())

parse_txt_to_csv()
# sentiments = open('sentiments.csv', 'w')
#
# sentiments.close()
