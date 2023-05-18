from core.api import BaseApi

from .index.viewsets.index import IndexViewset


def init(app) -> None:
    route = BaseApi(app, prefix="")
    route.add_resource(IndexViewset, "/")

    # api = BaseApi(app, prefix='/v1')
    # api.add_resource(IndexViewset, "/")
