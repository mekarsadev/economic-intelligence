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
            # standardized_data = yahoo.response.json()
            return yahoo.response.json(), yahoo.response.status_code
        except BaseException:
            return {"message": "yahoo service something wrong."}, 400

        # adj_close = standardized_data["chart"]["result"][0]["indicators"]["adjclose"][
        #     0
        # ]["adjclose"]

        # standardized_data["chart"]["result"][0]["indicators"]["adjclose"][0][
        #     "adjclose"
        # ] = self.standardized_outliers(data=adj_close)

        # return standardized_data, yahoo.response.status_code

    def standardized_outliers(self, data, threshold=3):
        data = self.fill_nul(data)

        if request.args.to_dict()["ticker"] == "JPYIDR=x":
            mean = np.nanmean(data)
            std = np.nanstd(data)
            z_scores = (data - mean) / std
            outliers = np.abs(z_scores) > threshold
            standardized_data = np.copy(data)
            standardized_data[
                outliers
            ] = mean  # Menggantikan outlier dengan nilai rata-rata

            return standardized_data.tolist()

        return data

    def fill_nul(self, data):
        # Mengisi data null dengan nilai di antara kedua angka
        for i in range(len(data)):
            if data[i] is None:
                j = i + 1
                while data[j] is None:
                    j += 1
                start_value = data[i - 1]
                end_value = data[j]
                increment = (end_value - start_value) / (j - i + 1)
                for k in range(i, j):
                    data[k] = start_value + increment * (k - i + 1)
        return data
        # before_index = None
        # after_index = None

        # for i in range(len(data)):
        #     if data[i] is not None:
        #         if before_index is None:
        #             before_index = i
        #         else:
        #             after_index = i
        #             break
        #     print(f"index {i} before -> {before_index} after -> {after_index}")

        # start_value = data[before_index]
        # end_value = data[after_index]

        # print(start_value, end_value)

        # for i in range(len(data)):
        #     if data[i] is None:
        #         data[i] = (start_value + end_value) / 2
        #         print(data[i])

        # return data
