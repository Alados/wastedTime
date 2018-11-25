import requests


class ProxyManager:
    def __init__(self):
        self._current_proxy = ""
        self._current_proxy_index = -1
        self._proxy_list = []
        self._get_proxy_list()

    def get_proxies(self):
        proxies = {
            "http": self._current_proxy,
            "https": self._current_proxy
        }

        return proxies

    def update_proxy(self):
        self._current_proxy_index += 1
        if self._current_proxy_index == len(self._proxy_list):
            print("Proxies are ended")
            print("Try get alternative proxy")
            proxy_ip_with_port = self._get_another_proxy()
            print("Proxy updated to " + proxy_ip_with_port)

            self._current_proxy = f'http://{proxy_ip_with_port}'
            return self._current_proxy

        proxy_ip_with_port = self._proxy_list[self._current_proxy_index]

        print("Proxy updated to " + proxy_ip_with_port)

        self._current_proxy = f'http://{proxy_ip_with_port}'
        return self._current_proxy

    @staticmethod
    def _get_another_proxy():
        proxy_response = requests.get("https://api.getproxylist.com/proxy?protocol[]=http", headers={
            'Content-Type': 'application/json'
        }).json()

        ip = proxy_response['ip']
        port = proxy_response['port']
        proxy = f'{ip}:{port}'

        return proxy

    def _get_proxy_list(self):
        proxy_response = requests.get("http://www.freeproxy-list.ru/api/proxy?anonymity=false&token=demo")
        self._proxy_list = proxy_response.text.split("\n")
