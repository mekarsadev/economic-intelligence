from core.api import BaseApi

from .analyzer.viewsets.predict import PredictViewset
from .index.viewsets.index import IndexViewset
from .ofx.viewsets.ofx import OFXViewset
from .yahoo.viewsets.yahoo import YahooViewset


def init(app) -> None:
    route = BaseApi(app, prefix="")
    route.add_resource(IndexViewset, "/")

    api = BaseApi(app, prefix="/v1/finet")
    api.add_resource(YahooViewset, "/yahoo/charts")
    api.add_resource(OFXViewset, "/ofx/charts")
    api.add_resource(PredictViewset, "/analyzer/predict")
