import requests

# class YahooBaseAPI:

#     def __init__(self, ticker, start_date, end_date):
#         self.start_date = start_date
#         self.end_date = end_date
#         self.ticker = ticker
#         self.headers = {}
#         self.payloads = {}
#         self.response = {}

#     def fetch(self):
#         pass


class YahooAPI:
    def __init__(self, ticker, start_date, end_date):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.yahoo_url = f"https://query1.finance.com/v8/finance/chart/{self.ticker}"
        self.payloads = ""
        self.querystring = {
            "symbol": self.ticker,
            "period1": self.start_date,
            "period2": self.end_date,
            "useYfid": "true",
            "interval": "1d",
            "includePrePost": "true",
            "events": "div|split|earn",
            "lang": "en-US",
            "region": "US",
            "crumb": "w9i.t0j2kw7",
            "corsDomain": "finance.yahoo.com",
        }
        self.headers = {
            "authority": "query1.finance.yahoo.com",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "en-US,en;q=0.9,id;q=0.8",
            "cache-control": "max-age=0",
            "cookie": "A1=d=AQABBKqfJWQCEDpSZ-uN12pK1lHnQu1TQvYFEgEBCAFKZmSYZFpOb2UB_eMBAAcIqp8lZO1TQvY&S=AQAAAt9UibOo5Jy4DYCyFpy2oyo; A3=d=AQABBKqfJWQCEDpSZ-uN12pK1lHnQu1TQvYFEgEBCAFKZmSYZFpOb2UB_eMBAAcIqp8lZO1TQvY&S=AQAAAt9UibOo5Jy4DYCyFpy2oyo; gam_id=y-f4SyeoZE2uIfJG3d5u5Vavfri9WdsdfC~A; tbla_id=3c61cfc4-7e28-4631-8d9b-f5f9e85ba691-tuctb2145d6; B=fcgijtli2b7ta&b=3&s=nn; GUC=AQEBCAFkZkpkmEIjmgTt; thamba=2; PRF=newChartbetateaser%3D1%26t%3DCNYIDR%253DX%252BUSDIDR%253DX%252BJPYIDR%253DX%252BJPY%253DX%252BSGD%253DX%252BIDR%253DX%252BSGDJPY%253DX%26qct%3Dcandle; cmp=t=1684357429&j=0&u=1---; A1S=d=AQABBKqfJWQCEDpSZ-uN12pK1lHnQu1TQvYFEgEBCAFKZmSYZFpOb2UB_eMBAAcIqp8lZO1TQvY&S=AQAAAt9UibOo5Jy4DYCyFpy2oyo&j=WORLD; SL_G_WPT_TO=id; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1",
            "dnt": "1",
            "sec-ch-ua-mobile": "?0",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        }

    def fetch(self):
        print(
            {
                "yahoo": self.yahoo_url,
                "data": self.payloads,
                # "headers": self.headers,
                "params": self.querystring,
            }
        )
        self.request = {}
        # self.response = requests.request("GET", self.yahoo_url, params=self.querystring)

        url = "https://query1.finance.yahoo.com/v8/finance/chart/" + self.ticker

        querystring = {
            "symbol": self.ticker,
            "period1": self.start_date,
            "period2": self.end_date,
            "useYfid": "true",
            "interval": "1d",
            "includePrePost": "true",
            "events": "div|split|earn",
            "lang": "en-US",
            "region": "US",
            "crumb": "w9i.t0j2kw7",
            "corsDomain": "finance.yahoo.com",
        }

        payload = ""
        headers = {
            "authority": "query1.finance.yahoo.com",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "en-US,en;q=0.9,id;q=0.8",
            "cache-control": "max-age=0",
            "cookie": "A1=d=AQABBKqfJWQCEDpSZ-uN12pK1lHnQu1TQvYFEgEBCAFKZmSYZFpOb2UB_eMBAAcIqp8lZO1TQvY&S=AQAAAt9UibOo5Jy4DYCyFpy2oyo; A3=d=AQABBKqfJWQCEDpSZ-uN12pK1lHnQu1TQvYFEgEBCAFKZmSYZFpOb2UB_eMBAAcIqp8lZO1TQvY&S=AQAAAt9UibOo5Jy4DYCyFpy2oyo; gam_id=y-f4SyeoZE2uIfJG3d5u5Vavfri9WdsdfC~A; tbla_id=3c61cfc4-7e28-4631-8d9b-f5f9e85ba691-tuctb2145d6; B=fcgijtli2b7ta&b=3&s=nn; GUC=AQEBCAFkZkpkmEIjmgTt; thamba=2; PRF=newChartbetateaser%3D1%26t%3DCNYIDR%253DX%252BUSDIDR%253DX%252BJPYIDR%253DX%252BJPY%253DX%252BSGD%253DX%252BIDR%253DX%252BSGDJPY%253DX%26qct%3Dcandle; cmp=t=1684357429&j=0&u=1---; A1S=d=AQABBKqfJWQCEDpSZ-uN12pK1lHnQu1TQvYFEgEBCAFKZmSYZFpOb2UB_eMBAAcIqp8lZO1TQvY&S=AQAAAt9UibOo5Jy4DYCyFpy2oyo&j=WORLD; SL_G_WPT_TO=id; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1",
            "dnt": "1",
            "sec-ch-ua-mobile": "?0",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        }

        self.response = requests.request(
            "GET", url, data=payload, headers=headers, params=querystring
        )
        print(self.response.status_code)


# print("response", self.response.status_code)
