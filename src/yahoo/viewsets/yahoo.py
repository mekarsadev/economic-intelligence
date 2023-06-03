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
        print("type ->", type(data))
        mean = np.mean(data)
        std = np.std(data)
        z_scores = (data - mean) / std
        outliers = np.abs(z_scores) > threshold
        standardized_data = np.copy(data)
        standardized_data[
            outliers
        ] = mean  # Menggantikan outlier dengan nilai rata-rata

        return standardized_data.tolist()
