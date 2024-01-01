import requests
# import asyncio

class Crypto_price_getter:
    def __init__(self, config):
        self.config = config

    def handle_error(self, error_msg):
        print(f'An error occured: {error_msg}')

    def get_each_token_price(self, coin_id):
        """
        test platform name : CoinMarketCap
        """
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': self.config['CoinMarketCap']['key']
        }

        options = {
            'amount': 1,
            'id': coin_id,
            'convert': 'TWD'
        }

        url = self.config['CoinMarketCap']['url']
        response = requests.get(url, headers=headers, params=options)

        if response.status_code == 200:
            data = response.json()

            if 'data' in data:
                name = data['data']['name']
                price = data['data']['quote']['TWD']['price']
                return name, price

            else:
                print('No data found in response.')
        else:
            print('Request failed with status code', response.status_code)
    
    def get_crypto_currency(self, crypto_code_df):

        coin_id_list = crypto_code_df['Coin ID'].tolist()
        crypto_data_price = []

        for id in coin_id_list:
            name, price = self.get_each_token_price(id)
            crypto_data_price.append({'Coin name': name, 'Coin Price':price})

        return crypto_data_price
    
