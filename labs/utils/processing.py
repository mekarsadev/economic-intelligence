import numpy as np
from sklearn.preprocessing import MinMaxScaler


def split_dataset(data, train_size=0.8):
    """
    reshaping dataset with ;
    80% training and 20% testing
    """

    n_data = len(data)
    x_ = data.value.iloc[: round(train_size * n_data)].values
    y_ = data.value.iloc[round(train_size * n_data) :].values
    return x_, y_


def minmax_normalization(data):
    """
    Scaling data with range above -1 up to 1
    """
    scaler = MinMaxScaler(feature_range=(-1, 1))
    scaled_data = scaler.fit_transform(data)
    return scaled_data


def sliding_window(data, window):
    X_ = []
    y_ = []

    for i in range(window, data.shape[0]):
        X_.append(data[i - window : i])
        y_.append(data[i])

    X_, y_ = np.array(X_), np.array(y_)
    return X_, y_
