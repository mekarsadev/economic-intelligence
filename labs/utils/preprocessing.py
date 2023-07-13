import os

import numpy as np
import yaml
from sklearn.preprocessing import MinMaxScaler


class CustomMinMaxScaler:
    def __init__(self, min_val, max_val, config_file):
        self.yaml_dir = os.path.join(os.getcwd(), config_file)
        with open(self.yaml_dir, "rb") as file:
            self.config = yaml.safe_load(file)
        self.min_val = min_val
        self.max_val = max_val
        self.min_data = self.config["DATA"]["MIN_DATA"]
        self.max_data = self.config["DATA"]["MAX_DATA"]

    def fit(self, data):
        self.min_data = min(data)
        self.max_data = max(data)
        self.config["DATA"]["MIN_DATA"] = self.min_data
        self.config["DATA"]["MAX_DATA"] = self.max_data
        with open(self.yaml_dir, "w") as file:
            yaml.dump(self.config, file)

    def transform(self, data):
        scaled_data = (data - self.min_data) / (self.max_data - self.min_data)
        scaled_data = scaled_data * (self.max_val - self.min_val) + self.min_val
        return scaled_data

    def list_transform(self, data):
        scaled_data = []
        for value in data:
            norm_ = (value - self.min_data) / (self.max_data - self.min_data)
            norm_ = norm_ * (self.max_val - self.min_val) + self.min_val
            scaled_data.append(norm_)
        return scaled_data

    def inverse_transform(self, scaled_data, min_data=None, max_data=None):
        if min_data:
            self.min_data = min_data
        if max_data:
            self.max_data = max_data

        data = (scaled_data - self.min_val) / (self.max_val - self.min_val)
        data = data * (self.max_data - self.min_data) + self.min_data
        return data


# function to create train, test data given stock data and sequence length
def load_data(stock, look_back):
    look_back += 1
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


class MinMaxScale:
    def __init__(self):
        self.scaler = MinMaxScaler(feature_range=(-1, 1))
        self.norm = []
        self.denorm = []

    def minmax_normalization(self, data, feature=""):
        data = data[[feature]]
        scaled_data = self.scaler.fit_transform(data)
        data["scaled"] = scaled_data[:]
        self.norm = data

    def minmax_denormalization(self, data, feature=""):
        scaled_data = self.scaler.inverse_transform(data)
        self.denorm = scaled_data


def minmax_normalization(data, feature="adj_close"):
    """
    Scaling data with range above -1 up to 1
    """

    data = data[[feature]]
    scaler = MinMaxScaler(feature_range=(-1, 1))
    scaled_data = scaler.fit_transform(data)
    data["scaled"] = scaled_data[:]
    return data


def minmax_denormalization(data, feature="adj_close"):
    scaler = MinMaxScaler(feature_range=(-1, 1))
    scaled_data = scaler.inverse_transform(data)
    return scaled_data


def sliding_window(data, window):
    X_ = []
    y_ = []

    for i in range(window, data.shape[0]):
        X_.append(data[i - window : i])
        y_.append(data[i])

    X_, y_ = np.array(X_), np.array(y_)
    return X_, y_
