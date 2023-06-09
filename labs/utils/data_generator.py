import pandas as pd
import requests

from .time import str2unix


def dataset_loader(start_date: int, end_date: int, ticker="JPY=X"):
    url = "https://api.mekarsa.com/v1/finet/yahoo/charts"
    querystring = {"start_date": start_date, "end_date": end_date, "ticker": ticker}
    try:
        response = requests.request(method="GET", url=url, params=querystring)
        return response
    except BaseException as error:
        return str(error)


def ofx_loader(start_date, end_date, scc, bcc):
    url = "https://api.mekarsa.com/v1/finet/ofx/charts"

    querystring = {
        "start_date": start_date,
        "end_date": end_date,
        "scc": scc,
        "bcc": bcc,
    }

    try:
        response = requests.request("GET", url, params=querystring)
        return response
    except BaseException as error:
        return str(error)


def ofx_dataset(start_date, end_date, scc="USD", bcc="IDR") -> pd.DataFrame:
    if isinstance(start_date, str):
        start_date = str2unix(start_date) * 1000

    if isinstance(end_date, str):
        end_date = str2unix(end_date) * 1000

    response = ofx_loader(start_date, end_date, scc, bcc)
    print(response.status_code)
    if response.status_code < 400:
        data_series = response.json()["data"]["HistoricalPoints"]
    else:
        print(response.status_code, response.text)
    df = pd.DataFrame(data_series)
    return df


def dataset_generator(start_date, end_date, ticker) -> pd.DataFrame:
    if isinstance(start_date, str):
        start_date = str2unix(start_date)

    if isinstance(end_date, str):
        end_date = str2unix(end_date)

    data_json = dataset_loader(start_date, end_date, ticker)
    if isinstance(data_json, str):
        print(data_json)
    elif data_json.status_code >= 400 and data_json < 500:
        print(data_json.json())
    elif data_json.status_code >= 500:
        print(data_json)

    chart = data_json.json()
    data_timestamp = chart["data"]["chart"]["result"][0]["timestamp"]
    data_series = chart["data"]["chart"]["result"][0]["indicators"]["quote"][0]
    data_series["adj_close"] = chart["data"]["chart"]["result"][0]["indicators"][
        "adjclose"
    ][0]["adjclose"]
    print()

    df = pd.DataFrame(data_series, index=data_timestamp)

    return df
