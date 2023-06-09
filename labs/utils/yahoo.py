from datetime import datetime

import pandas as pd
import requests

from labs.utils.parser import datestring2unix


class Yahoo:
    def __init__(self) -> None:
        self.querystring = {}
        self.payload = {}
        self.headers = {
            "authority": "query1.finance.yahoo.com",
            "accept": "*/*",
            "dnt": "1",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "ubuntu",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        }


class YahooCurrencies(Yahoo):
    def __init__(
        self, symbol="USDIDR=X", interval="1d", start_date=None, end_date=None
    ) -> None:
        super().__init__()
        start_date = datestring2unix("2020-01-01")
        end_date = datestring2unix(datetime.today())
        self.url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
        self.querystring = {
            "symbol": symbol,
            "period1": str(start_date),
            "period2": end_date,
            "useYfid": "true",
            "interval": interval,
            "includePrePost": "true",
            "events": "div|split|earn",
            "lang": "en-US",
            "region": "US",
            "crumb": "w9i.t0j2kw7",
            "corsDomain": "finance.yahoo.com",
        }
        self.payload = ""

    def fetch_histories(self) -> None:
        response = requests.request(
            "GET", url=self.url, headers=self.headers, params=self.querystring
        )
        self.response = response
        print(response.status_code)
        if response.status_code >= 400:
            raise BaseException("Data fetching has been failed.")

    def fetch_dateframe(self) -> None:
        self.dataset = pd.DataFrame()
        self.dataset["timestamp"] = self.response.json()["chart"]["result"][0][
            "timestamp"
        ]

        indicators = self.response.json()["chart"]["result"][0]["indicators"]["quote"][
            0
        ]

        for k, v in indicators.items():
            self.dataset[k] = v

        self.dataset.set_index("timestamp")
