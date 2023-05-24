import pandas as pd
import requests

from .time import str2unix


def dataset_loader(start_date: int, end_date: int, ticker="JPY=X"):
    url = "https://api.mekarsa.com/v1/finet/yahoo/charts"
    querystring = {"start_date": start_date, "end_date": end_date, "ticker": ticker}
    try:
        print("fetch...", querystring)
        response = requests.request(method="GET", url=url, params=querystring)
        print(response.json())
        return response
    except BaseException as error:
        return str(error)


def dataset_generator(start_date, end_date, ticker) -> pd.DataFrame:
    if isinstance(start_date, str):
        start_date = str2unix(start_date)

    if isinstance(end_date, str):
        end_date = str2unix(end_date)

    data_json = dataset_loader(start_date, end_date, ticker)
    print(data_json)
    if isinstance(data_json, str):
        print(data_json)
    elif data_json.status_code >= 400 and data_json < 500:
        print(data_json.json())
    elif data_json.status_code >= 500:
        print(data_json)

    chart = data_json.json()
    data_timestamp = chart["data"]["chart"]["result"][0]["timestamp"]
    data_series = chart["data"]["chart"]["result"][0]["indicators"]["quote"][0]

    df = pd.DataFrame(data_series, index=data_timestamp)

    return df
