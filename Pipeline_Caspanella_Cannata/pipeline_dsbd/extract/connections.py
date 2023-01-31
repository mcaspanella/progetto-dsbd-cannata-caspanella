from prometheus_api_client import PrometheusConnect
import requests, urllib3
import subprocess

url = "http://15.160.61.227:29090"


def connect():
    response = subprocess.run(["curl", "-I", url], capture_output=True, text=True)
    status_code = response.returncode
    if status_code == 0:
        print(f"URL {url} è valido")
        prom = PrometheusConnect(url =url, disable_ssl=True) 
        return prom
    else:
        print(f"URL {url} non è valido")