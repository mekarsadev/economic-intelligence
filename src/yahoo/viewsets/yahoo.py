import numpy as np
from flask import request
from flask_restful import Resource
from yahoo.helpers.api import YahooAPI


class YahooViewset(Resource):
    def get(self):
        params = request.args.to_dict()
        yahoo = YahooAPI(**params)
        yahoo.fetch()

        try:
            standardized_data = yahoo.response.json()
            # return yahoo.response.json(), yahoo.response.status_code
        except BaseException:
            return {"message": "yahoo service something wrong."}, 400

        adj_close = standardized_data["chart"]["result"][0]["indicators"]["adjclose"][
            0
        ]["adjclose"]

        standardized_data["chart"]["result"][0]["indicators"]["adjclose"][0][
            "adjclose"
        ] = self.standardized_outliers(data=adj_close)

        return standardized_data, yahoo.response.status_code

    def standardized_outliers(self, data, threshold=3):
        data = self.fill_nul(data)
        mean = np.mean(data)
        std = np.std(data)
        z_scores = (data - mean) / std
        outliers = np.abs(z_scores) > threshold
        standardized_data = np.copy(data)
        standardized_data[
            outliers
        ] = mean  # Menggantikan outlier dengan nilai rata-rata

        return standardized_data.tolist()

    def fill_nul(self, data):
        before_index = None
        after_index = None

        for i in range(len(data)):
            if data[i] is not None:
                if before_index is None:
                    before_index = i
                else:
                    after_index = i
                    break

        start_value = data[before_index]
        end_value = data[after_index]

        for i in range(len(data)):
            if data[i] is None:
                data[i] = (start_value + end_value) / 2

        return data
