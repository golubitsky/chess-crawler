import os
import sys

from src.http_client import HttpClient
from src.async_client import AsyncHttpClient as HttpClient

from flask import Flask
app = Flask(__name__)

workers = os.environ['WORKERS'] or 1
workers = int(workers)

threads = os.environ['THREADS'] or 1
threads = int(threads)

@app.route("/")
def hello():
    http_client = HttpClient('http://httpbin.org/', workers, threads)
    futures = [http_client.get('get') for _ in range(10)]
    results = map(lambda f: f.result().json(), futures)
    return str(len(list(results)))

@app.route('/chess')
def chess():
    http_client = HttpClient('http://www.chessgames.com/', workers, threads)
    r = http_client.get('').result()
    return r.text

if __name__ == "__main__":
    app.run(host='0.0.0.0')
