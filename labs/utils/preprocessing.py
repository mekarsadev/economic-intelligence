import numpy as np
from sklearn.preprocessing import MinMaxScaler


# function to create train, test data given stock data and sequence length
def load_data(stock, look_back):
    data_raw = stock.values  # convert to numpy array
    data = []

    # create all possible sequences of length look_back
    for index in range(len(data_raw) - look_back):
        data.append(data_raw[index : index + look_back])

    data = np.array(data)
    test_set_size = int(np.round(0.2 * data.shape[0]))
    train_set_size = data.shape[0] - (test_set_size)

    x_train = data[:train_set_size, :-1, :]
    y_train = data[:train_set_size, -1, :]

    x_test = data[train_set_size:, :-1]
    y_test = data[train_set_size:, -1, :]

    print("X_train size", x_train.shape)
    print("y_train size", y_train.shape)
    print("X_test size", x_test.shape)
    print("y_test size", y_test.shape)

    return x_train, y_train, x_test, y_test


def minmax_normalization(data):
    """
    Scaling data with range above -1 up to 1
    """

    data = data[["close"]]
    scaler = MinMaxScaler(feature_range=(-1, 1))
    scaled_data = scaler.fit_transform(data)
    data["scaled"] = scaled_data[:]
    return data


def sliding_window(data, window):
    X_ = []
    y_ = []

    for i in range(window, data.shape[0]):
        X_.append(data[i - window : i])
        y_.append(data[i])

    X_, y_ = np.array(X_), np.array(y_)
    return X_, y_
