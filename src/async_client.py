from concurrent.futures import ThreadPoolExecutor
from requests_futures.sessions import FuturesSession

class AsyncHttpClient():
    def __init__(self, base_url, workers=1, threads=1):
        self.base_url = base_url
        self.session = FuturesSession(
            executor=ThreadPoolExecutor(max_workers=threads))

    def get(self, path):
        url = self.base_url + path
        return self.session.get(url)