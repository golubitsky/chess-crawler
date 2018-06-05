from concurrent.futures import ThreadPoolExecutor
from requests_futures.sessions import FuturesSession

class AsyncHttpClient():
    def __init__(self, base_url, workers=1, threads=1):
        self.base_url = base_url
        self.session = FuturesSession(
            executor=ThreadPoolExecutor(max_workers=threads))

    def get(self, path, query_string_params={}):
        qsp = "?"
        for k in query_string_params:
            qsp += f"{k}={query_string_params[k]}&"

        url = self.base_url + path + qsp
        print(url)
        return self.session.get(url)