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
        url = f"https://api.ofx.com/PublicSite.ApiService//SpotRateHistory/{self.scc}/{self.bcc}/{self.start_date}/{self.end_date}"

        headers = {
            "cookie": "AWSALB=im7M9BzJ03Mq7i1ap4yAh2GuXbGpTfZkF5%2BbE2Y6C1yuCyCXjQPkpjntorRhqtIib7SPD2j5%2FHyxjQtutA%2BxoqOaZQg7iFXQU92Iel3Up2ZklGGPOmHj3Vuy%2F9ub; AWSALBCORS=im7M9BzJ03Mq7i1ap4yAh2GuXbGpTfZkF5%2BbE2Y6C1yuCyCXjQPkpjntorRhqtIib7SPD2j5%2FHyxjQtutA%2BxoqOaZQg7iFXQU92Iel3Up2ZklGGPOmHj3Vuy%2F9ub",
            "authority": "api.ofx.com",
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9,id;q=0.8",
            "dnt": "1",
            "origin": "https://www.ofx.com",
            "referer": "https://www.ofx.com/",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        }

        response = requests.request(
            "GET", url, data="", headers=headers, params=self.querystring
        )
        self.data = response
