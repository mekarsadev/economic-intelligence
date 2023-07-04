import time
from datetime import datetime, timedelta

import torch
from flask_restful import Resource, request

from labs.utils.data_generator import ofx_dataset
from src.analyzer.lstm import LSTMModel


class PredictViewset(Resource):

    TICKERS = ["USDIDR=x", "JPYIDR=x"]

    def post(self):
        data = request.get_json()

        lstm = LSTMModel(input_size=1, hidden_sizes=[32], output_size=1)
        lstm.load_state_dict(torch.load("labs/models/USD/best.pth"))

        if data["model"] not in self.TICKERS:
            return {"message": "ticker not available."}, 400

        predicted_values = []
        predicted_timestamp = []
        timestamp = int(time.time())

        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=10)

        end_date = end_date.strftime("%Y-%m-%d")
        start_date = start_date.strftime("%Y-%m-%d")
        ofx_sample = ofx_dataset(start_date, end_date)

        for i in range(10):
            timestamp += 86400
            predicted_timestamp.append(timestamp)
            predicted_values.append(ofx_sample[["values"]].values[i][0])

        response = {"timetamp": predicted_timestamp, "values": predicted_values}
        return response
