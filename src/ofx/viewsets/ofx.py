from flask_restful import Resource, request

from ofx_modules.api import OFX


class OFXViewset(Resource):
    def get(self):
        params = request.args.to_dict()
        ofx = OFX(**params)
        print("fetch...", ofx)
        ofx.fetch()

        response = ofx.data.json().copy()
        response["HistoricalPoints"] = self.generateXY(response["HistoricalPoints"])
        return response, ofx.data.status_code

    def generateXY(self, data):
        buckets = {"timestamps": [], "values": []}

        for daily in data:
            buckets["timestamps"].append(int(daily["PointInTime"] / 1000))
            buckets["values"].append(daily["InterbankRate"])

        return buckets
