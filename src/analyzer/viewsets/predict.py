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
        predict_size = data.get("length", 100)
        ticker_ = "USD" if data["model"] == "USDIDR=x" else "JPY"
        config_file = "labs/config.yaml" if ticker_ == "USD" else "labs/config-jpy.yaml"

        with open(config_file, "rb") as file:
            config = yaml.safe_load(file)

        INPUT = config["MODEL"]["CHECKPOINT"]["INPUT"]
        HIDDEN_1 = config["MODEL"]["CHECKPOINT"]["HIDDEN_1"]
        HIDDEN_2 = config["MODEL"]["CHECKPOINT"]["HIDDEN_2"]

        print(INPUT, HIDDEN_1, HIDDEN_2)

        # load data trigger
        trigger_test = []
        end_date = datetime.now() - timedelta(days=7)
        current = int(time.mktime(end_date.timetuple()))

        if "trigger" in data:
            trigger_test = data["trigger"]
        else:
            start_date = data["start_preview"] * 1000
            end_date = data["end_preview"] * 1000

            ofx_sample = ofx_dataset(start_date, end_date, scc=ticker_)
            for rate in ofx_sample[["values"]].values:
                trigger_test.append(rate[0])

        lstm = LSTMModel(input_size=1, hidden_sizes=[HIDDEN_1, HIDDEN_2], output_size=1)
        lstm.load_state_dict(
            torch.load(f"labs/models/{ticker_}/{INPUT}_{HIDDEN_1}_{HIDDEN_2}.pth")
        )

        if data["model"] not in self.TICKERS:
            return {"message": "ticker not available."}, 400

        # get trigger data test

        # normalization trigeer data test
        data_scaler = CustomMinMaxScaler(min_val=-1, max_val=1, config_file=config_file)
        normalized = data_scaler.list_transform(trigger_test)

        # sliding window trigger data test
        X_input = self.sliding_window(normalized, window_size=INPUT)

        with torch.no_grad():
            predicted_timestamp = []
            new_predicted = []
            for _ in range(predict_size):
                input_sequence = torch.Tensor(X_input)
                predicted = lstm(input_sequence)

                # insert last predict to new X data rows
                _new = torch.Tensor([predicted[-1]])
                X_new = torch.cat((X_input[-1][1:], _new.view(1, 1)), dim=0)
                X_input = torch.cat((X_input, X_new.view(1, X_new.shape[0], 1)), dim=0)

                predicted_denorm = data_scaler.inverse_transform(predicted)

                new_predicted.append(predicted_denorm[-1].item())
                current += 86400
                predicted_timestamp.append(current)

            # for _ in range(7):
            #     prediction = lstm(input_sequence)
            #     predicted_list.append(data_scaler.inverse_transform(prediction.item()))

            #     current += 86400
            #     predicted_timestamp.append(current)

            #     input_sequence = torch.cat(
            #         (input_sequence[:, 1:, :], prediction.unsqueeze(0)), dim=1
            #     )

        # response = {"timestamp": predicted_timestamp, "values": predicted_denorm.flatten().tolist()}
        response = {"timestamp": predicted_timestamp, "values": new_predicted}
        return response

    # Modul Sliding Window
    def sliding_window(self, data, window_size):
        X = []
        for i in range(len(data) - window_size):
            X.append(data[i : i + window_size])
        X = np.array(X)
        X_reshape = X.reshape(X.shape[0], X.shape[1], 1)
        return torch.from_numpy(X_reshape).type(torch.Tensor)
