import time
from datetime import datetime, timedelta

import numpy as np
import torch
import yaml
from flask_restful import Resource, request

from labs.utils.data_generator import ofx_dataset
from labs.utils.preprocessing import CustomMinMaxScaler
from src.analyzer.lstm import LSTMModel


class PredictViewset(Resource):

    TICKERS = ["USDIDR=x", "JPYIDR=x"]

    def post(self):
        data = request.get_json()
        ticker_ = "USD" if data["model"] == "USDIDR=x" else "JPYIDR=x"
        config_file = "labs/config.yaml" if ticker_ == "USD" else "labs/config-jpy.yaml"

        with open(config_file, "rb") as file:
            config = yaml.safe_load(file)

        INPUT = config["MODEL"]["CHECKPOINT"]["INPUT"]
        HIDDEN_1 = config["MODEL"]["CHECKPOINT"]["HIDDEN_1"]
        HIDDEN_2 = config["MODEL"]["CHECKPOINT"]["HIDDEN_2"]

        lstm = LSTMModel(input_size=1, hidden_sizes=[HIDDEN_1, HIDDEN_2], output_size=1)
        lstm.load_state_dict(
            torch.load(f"labs/models/{ticker_}/{INPUT}_{HIDDEN_1}_{HIDDEN_2}.pth")
        )

        if data["model"] not in self.TICKERS:
            return {"message": "ticker not available."}, 400

        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=30)
        current = int(time.mktime(end_date.timetuple()))

        end_date = end_date.strftime("%Y-%m-%d")
        start_date = start_date.strftime("%Y-%m-%d")

        ofx_sample = ofx_dataset(start_date, end_date)

        # get trigger data test
        trigger_test = []
        for rate in ofx_sample[["values"]].values:
            trigger_test.append(rate[0])

        # normalization trigeer data test
        data_scaler = CustomMinMaxScaler(min_val=-1, max_val=1)
        normalized = data_scaler.list_transform(trigger_test)

        # sliding window trigger data test
        X_input = self.sliding_window(normalized, window_size=INPUT)

        with torch.no_grad():
            predicted_list = []
            predicted_timestamp = []
            input_sequence = torch.Tensor(X_input[-1:])

            for _ in range(7):
                prediction = lstm(input_sequence)
                predicted_list.append(data_scaler.inverse_transform(prediction.item()))
                predicted_timestamp.append(current)

                current += 86400

                input_sequence = torch.cat(
                    (input_sequence[:, 1:, :], prediction.unsqueeze(0)), dim=1
                )

        response = {"timestamp": predicted_timestamp, "values": predicted_list}
        return response

    # Modul Sliding Window
    def sliding_window(self, data, window_size):
        X = []
        for i in range(len(data) - window_size):
            X.append(data[i : i + window_size])
        X = np.array(X)
        X_reshape = X.reshape(X.shape[0], X.shape[1], 1)
        return torch.from_numpy(X_reshape).type(torch.Tensor)
