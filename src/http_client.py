import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import logging
import sys
# use logging.DEBUG to debug HTTP low-level details
logging.basicConfig(level=logging.INFO)


class HttpClient():
    """
        Currently supports GET and POST requests (JSON body only).
        Features automatic retry on timeout and certain 50* codes.
        Capable of status_code specific logic.
        get() and post() methods return [Response, None] or [None, error].
    """
    default_timeout = 30

    class _Decorators(object):
        @classmethod
        def http_request_with_exception_handling(self, http_request_function):
            def send_request(self, path, **kwargs):
                try:
                    response = http_request_function(self, path, **kwargs)
                    self.last_url_requested = self._full_url(path)

                    # Treat non 2** status codes as RequestExceptions.
                    response.raise_for_status()

                    return [response, None]
                except requests.ConnectionError as e:
                    print(
                        f"A timeout occurred while attempting to issue a request to {self._full_url(path)}")
                    return [None, e]
                except requests.RequestException as e:
                    if e.response is not None:
                        # Generic non-200 response-handling here
                        status = e.response.status_code
                        if status >= 500:
                            pass
                        elif status >= 400:
                            pass
                        elif status >= 300:
                            pass

                    return [None, e]
                except KeyboardInterrupt as e:
                    print('\nKeyboardInterrupt: exiting application.')
                    sys.exit()
            return send_request

    def __init__(self, base_url, max_retries=5, timeout_seconds=-1):
        # Set Timeout (timeout=None is valid)
        self.timeout_seconds = timeout_seconds
        if self.timeout_seconds == -1:
            self.timeout_seconds = HttpClient.default_timeout

        # Base URL
        self.base_url = base_url

        # Retry Logic
        self.session = requests.Session()
        retries = Retry(total=max_retries, backoff_factor=0.5,
                        status_forcelist=[502, 503, 504])
        self.session.mount(base_url, HTTPAdapter(
            max_retries=retries))

        self.last_url_requested = None

    def _full_url(self, path):
        return self.base_url + path

    @_Decorators.http_request_with_exception_handling
    def get(self, path, timeout_seconds=-1):
        """
            For successful requests returns [response, None].
            For unsuccessful requests returns [None, error]
        """
        # timeout=None is valid
        if timeout_seconds == -1:
            timeout_seconds = self.timeout_seconds

        return self.session.get(self._full_url(path), timeout=timeout_seconds)

    @_Decorators.http_request_with_exception_handling
    def post(self, path, json={}, timeout_seconds=-1):
        # timeout_seconds=None is valid
        if timeout_seconds == -1:
            timeout_seconds = self.timeout_seconds

        return self.session.post(self._full_url(path), json, timeout=timeout_seconds)
