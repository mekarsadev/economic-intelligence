import requests


class OFX:
    def __init__(self, scc, bcc, start_date, end_date):
        self.scc = scc
        self.bcc = bcc
        self.start_date = start_date
        self.end_date = end_date
        self.querystring = {
            "DecimalPlace": 6,
            "ReportingInterval": "Daily",
            "format": "json",
        }

    def fetch(self):
        url = f"https://api.ofx.com/PublicSite.ApiService/SpotRateHistory/{self.scc}/{self.bcc}/{self.start_date}/{self.end_date}"

        headers = {
            "authority": "api.ofx.com",
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9,id;q=0.8",
            "dnt": "1",
            "origin": "https://www.ofx.com",
            "referer": "https://www.ofx.com/",
            "sec-ch-ua": "'Not.A/Brand';v='8', 'Chromium';v='114', 'Google Chrome';v='114'",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "'macOS'",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        }

        response = requests.request(
            "GET", url, data="", headers=headers, params=self.querystring
        )
        self.data = response
