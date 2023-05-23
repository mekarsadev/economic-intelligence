from flask import request
from flask_restful import Resource
from yahoo.helpers.api import YahooAPI


class YahooViewset(Resource):
    def get(self):
        params = request.args.to_dict()
        yahoo = YahooAPI(**params)
        yahoo.fetch()

        try:
            return yahoo.response.json(), yahoo.response.status_code
        except BaseException:
            return {"message": "yahoo service something wrong."}, 400
