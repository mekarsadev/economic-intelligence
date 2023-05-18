from flask_restful import Resource


class IndexViewset(Resource):
    def get(self, *args, **kwargs):
        return {"says": "Hello, world"}
