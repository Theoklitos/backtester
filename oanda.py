import requests

api_key = '?'
root_url = 'https://api-fxpractice.oanda.com'
account_id = '?'


class Oanda:
    def __init__(self, root_url):
        self.root_url = root_url

    def _make_request(self, url):
        url = '{}{}'.format(self.root_url, url)
        result = requests.get(url, headers={'Authorization': 'Bearer {}'.format(api_key)})
        return result

    def get_accounts(self):
        return self._make_request('/v3/accounts')
