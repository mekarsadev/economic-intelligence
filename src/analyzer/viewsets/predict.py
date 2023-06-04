import random
import time

from flask_restful import Resource, request


class PredictViewset(Resource):

    TICKERS = ["USDIDR=x", "JPYIDR=x"]

    def post(
        self,
    ):
        data = request.get_json()

        if data["model"] not in self.TICKERS:
            return {"message": "ticker not available."}, 400

        predicted_value = []
        predicted_timestamp = []
        timestamp = int(time.time())
        for _ in range(10):
            random_range = random.uniform(100.5, 240.5)
            timestamp += 86400
            predicted_timestamp.append(timestamp)
            predicted_value.append(round(random_range, 2))

        return {"timestamp": predicted_timestamp, "predicted_value": predicted_value}
