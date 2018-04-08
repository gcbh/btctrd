import time
import warnings
import numpy as np
from numpy import newaxis
import os
# from keras.models import Model
# from keras.layers import Input, LSTM, Dense
# import matplotlib.pyplot as plt

# 1522148299 - 1417412036

# 'coinbaseUSD.csv'
def load_bitcoin_prices(seq_len):
    DATASET_PATH = 'price_dataset.npz'
    if not os.path.exists(DATASET_PATH):
        start = 1514764800
        end = 1522148299
        data = [0 for i in range((end - start) // 300)] # every 5 minutes for 2017
        prev_val = -1
        print("opening CSV file...")
        f = open('coinbaseUSD.csv', 'r')
        raw_data = [row.split(',') for row in f.read().split('\n')]
        print('closing csv file...')
        f.close()
        print("raw data", raw_data[0])
        start = raw_data[0][0]
        print("start", start)
        print("end", start + total_epoch)
        for i in range(len(raw_data)):
            idx = (int(raw_data[i][0]) - start) // 300
            if idx < len(data) and idx > -1:
                data[idx] = raw_data[i][1]

        sequence_length = seq_len + 1
        price_result = []
        # volume_result = []
        for index in range(len(data) - sequence_length):
            price_result.append(data[index: index + sequence_length])

        result = np.array(price_result)

        row = round(0.9 * result.shape[0])
        train = result[:int(row), :]
        np.random.shuffle(train)
        x_train = train[:, :-1]
        y_train = train[:, -1]
        x_test = result[int(row): , :-1]
        y_test = result[int(row): , -1]

        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
        x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

        np.savez(DATASET_PATH, x_train, y_train, x_test, y_test)
        return [x_train, y_train, x_test, y_test]

    else:
        with np.load(DATASET_PATH) as data:
            return [data['x_train'], data['y_train'], data['y_test'], data['y_test']]


def load_sentiments(seq_len):
    DATASET_PATH = 'sentiment_dataset.npz'
    if not os.path.exists(DATASET_PATH):
        start = 1514764800
        end = 1522148299
        data = [0 for i in range((end - start) // 300)] # every 5 minutes for past 3 months
        print('opening csv...')
        f = open('sentiments.csv', 'r')
        raw_data = [row.split(',') for row in list(filter(None, f.read().split('\n')))]
        print('raw', len(raw_data))
        print('data', len(data))
        print('closing csv...')
        f.close()
        for i in range(len(raw_data)):
            idx = (int(raw_data[i][0]) - start) // 300
            if idx < len(data) and idx > -1:
                data[idx] = raw_data[i][1]
        print('parsing data done')
        sequence_length = seq_len + 1
        result = []

        for index in range(len(data) - sequence_length):
            result.append(data[index: index + sequence_length])

        print('batches done')

        result = np.array(result)

        row = round(0.9 * result.shape[0])
        train = result[:int(row), :]
        np.random.shuffle(train)
        x_train = train[:, :-1]
        y_train = train[:, -1]
        x_test = result[int(row): , :-1]
        y_test = result[int(row): , -1]

        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
        x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

        np.savez(DATASET_PATH, x_train, y_train, x_test, y_test)
        return [x_train, y_train, x_test, y_test]

    else:
        with np.load(DATASET_PATH) as data:
            return [data['x_train'], data['y_train'], data['y_test'], data['y_test']]

# Granularity: 5 minutes, dataLength = 5 minutes * 60 = 300 = 5 hrs
# labelLength = 4 = 20 minutes
def buildModel(dataLength, labelLength):
    price = Input(shape=(dataLength, 1), name='price')
    sentiment = Input(shape=(dataLength, 1), name='sentiment')

    priceLayers = LSTM(64, return_sequences=False)(price)
    sentimentLayers = LSTM(64, return_sequences=False)(sentiment)

    output = concatenate(
        [
            priceLayers,
            sentimentLayers,
        ]
    )

    output = Dense(labelLength, activation='linear', name='weightAverage_output')(output)

    model = Model(
        inputs =
        [
            price,
            sentiment,
        ],
        outputs =
        [
            output
        ]
    )

    model.compile(optimizer='rmsprop', loss='mse')

    return model

if __name__ == '__main__':
    # price_x_train, price_y_train, price_x_test, price_y_test = load_bitcoin_prices(60)
    sentiment_x_train, sentiment_y_train, sentiment_x_test, sentiment_y_test = load_sentiments(60)

    # rnn = buildModel(300, 20)
    #
    # rnn.fit(
    #     [
    #         trainingData["price"],
    #         trainingData["sentiment"],
    #     ],
    #     [
    #         trainingLabels["price"]
    #     ],
    #     validation_data=(
    #         [
    #             testingData["price"],
    #             testingData["sentiment"],
    #         ],
    #         [
    #             testingLabels["price"]
    #         ]),
    #     epochs=1,
    #     batch_size=300,
    #     callbacks=[
    #         board.createTensorboardConfig('logs/Graph'),
    #     ])
